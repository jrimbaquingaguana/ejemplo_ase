import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
import threading
from PIL import Image, ImageTk
import time

# Función para alternar la detección
def toggle_detection(event=None):
    global detection_active
    detection_active = not detection_active
    if detection_active:
        btn_toggle_detection.config(text="Detener Detección (D)", bg="#FF6347", fg="white", font=("Arial", 12, "bold"))
    else:
        btn_toggle_detection.config(text="Iniciar Detección (D)", bg="#32CD32", fg="white", font=("Arial", 12))

# Función para alternar la grabación
def toggle_recording(event=None):
    global recording_active, out, fps, start_time
    if recording_active:
        recording_active = False
        lbl_recording_status.config(text="Grabación terminada", bg="#228B22", fg="white", font=("Arial", 12))
        btn_toggle_recording.config(text="Iniciar Grabación (R)", bg="#32CD32", fg="white", font=("Arial", 12))
    else:
        recording_active = True
        start_time = time.time()  # Guardar el tiempo de inicio de la grabación
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('output.mp4', fourcc, fps, (int(cam.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))))  # Iniciar la grabación
        lbl_recording_status.config(text="Grabando...", bg="#DC143C", fg="white", font=("Arial", 12))
        btn_toggle_recording.config(text="Detener Grabación (R)", bg="#FF6347", fg="white", font=("Arial", 12, "bold"))

# Función para salir del programa
def quit_program(event=None):
    global root, out
    if recording_active:
        toggle_recording()
    root.destroy()
    if out is not None:
        out.release()

# Función principal para procesar la entrada de la cámara
def opencv_loop():
    global frame, detection_active, recording_active, out, fps, start_time
    while True:
        ret, frame = cam.read()
        if not ret:
            break  # Si no se puede leer la cámara, salir del bucle
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detección activa
        if detection_active:
            output = face_mesh.process(rgb_frame)
            landmark_points = output.multi_face_landmarks
            frame_h, frame_w, _ = frame.shape
            if landmark_points:
                landmarks = landmark_points[0].landmark
                for id, landmark in enumerate(landmarks[474:478]):
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 0))
                    if id == 1:
                        screen_x = (screen_w * landmark.x)
                        screen_y = (screen_h * landmark.y)
                        pyautogui.moveTo(screen_x, screen_y)

                # Detectar movimiento de los ojos para simular un click
                left = [landmarks[145], landmarks[159]]
                for landmark in left:
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 255))
                if (left[0].y - left[1].y) < 0.005:
                    pyautogui.click()
                    pyautogui.sleep(1)

        # Grabación activa
        if recording_active:
            current_time = time.time()
            elapsed_time = current_time - start_time  # Calcular el tiempo transcurrido
            formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))  # Formatear el tiempo transcurrido
            lbl_recording_status.config(text=f"Grabando... Tiempo: {formatted_time}", bg="#DC143C", fg="white", font=("Arial", 12))
            out.write(frame)

        # Actualizar la ventana con el frame actual
        if frame is not None:
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img = ImageTk.PhotoImage(image=img)
            label.configure(image=img)
            label.image = img
            label.update_idletasks()



#ANGELO INICIO
# Inicializar la cámara y MediaPipe Face Mesh
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

# Variables de control
detection_active = True  # Iniciar con la detección desactivada
recording_active = False  # No grabar hasta que se indique
out = None  # Inicializar el objeto VideoWriter como None
start_time = 0  # Inicializar el tiempo de inicio de grabación

# Obtener la tasa de fotogramas de la cámara
fps = cam.get(cv2.CAP_PROP_FPS)
print(f"Tasa de fotogramas de la cámara: {fps}")

# Crear la ventana de la interfaz gráfica
root = tk.Tk()
root.title("Eye Controlled Mouse")

# ANGELO FIN



# Definir el ancho de los botones
button_width = 20

# Configuración de estilo para los botones
btn_style = {"font": ("Arial", 12), "width": button_width}

# Botones para alternar detección, grabación y salir del programa
btn_toggle_detection = tk.Button(root, text="Iniciar Detección (D)", command=toggle_detection, bg="#32CD32", fg="white", **btn_style)
btn_toggle_detection.pack(side=tk.TOP, pady=5)

btn_toggle_recording = tk.Button(root, text="Iniciar Grabación (R)", command=toggle_recording, bg="#32CD32", fg="white", **btn_style)
btn_toggle_recording.pack(side=tk.TOP, pady=5)

btn_quit = tk.Button(root, text="Salir (Q)", command=quit_program, bg="#FF6347", fg="white", **btn_style)
btn_quit.pack(side=tk.TOP, pady=5)

# Etiqueta para mostrar el feed de la cámara
label = tk.Label(root)
label.pack()

# Etiqueta para mostrar el estado de la grabación
lbl_recording_status = tk.Label(root, text="", bg="white", font=("Arial", 12))
lbl_recording_status.pack(side=tk.BOTTOM, pady=5)

# Asociar eventos de teclado
root.bind('<KeyPress-d>', toggle_detection)
root.bind('<KeyPress-r>', toggle_recording)
root.bind('<KeyPress-q>', quit_program)

# Iniciar el bucle para procesar la entrada de la cámara en un hilo separado
thread = threading.Thread(target=opencv_loop, daemon=True)
thread.start()

# Iniciar el loop de la interfaz gráfica
root.mainloop()


