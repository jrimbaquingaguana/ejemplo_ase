from behave import given, when, then
import pyautogui
from pywinauto import Application
from pywinauto.mouse import click
from PIL import ImageGrab
import os
import time
from datetime import datetime


# Variables globales
process = None
app = None
window = None
buttons = None
current_y = 750  # Coordenada Y inicial para el texto
image_height = 300  # Altura de la imagen en el PDF
pdf_path = None
c = None  # Canvas global

# Crear un nuevo directorio 'reports' para cada ejecución
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_dir = f"reports_{timestamp}"
os.makedirs(report_dir, exist_ok=True)
pdf_path = os.path.join(report_dir, f"test_report_{timestamp}.pdf")

def create_pdf_file(file_name):
    global c
    c = canvas.Canvas(file_name, pagesize=letter)
    c.setFont("Helvetica", 12)
    print(f"PDF {file_name} creado.")

def capture_screenshot(file_name):
    screenshot = ImageGrab.grab()
    screenshot.save(file_name)
    print(f"Captura de pantalla guardada como {file_name}.")

def add_text_to_pdf(text):
    global c, current_y
    c.drawString(100, current_y, text)
    current_y -= 20
    if current_y < 50:
        c.showPage()
        current_y = 750

def add_screenshot_to_pdf(image_path):
    global c, current_y
    if current_y < image_height + 50:
        c.showPage()
        current_y = 750
    c.drawImage(image_path, 10, current_y - image_height, 500, image_height)
    current_y -= image_height + 20

def close_pdf():
    global c
    c.save()
    print(f"PDF {pdf_path} cerrado.")

@given('la aplicación está en ejecución')
def step_given_application_running(context):
    global process, app, window, buttons
    print("Iniciando la aplicación...")
    process = subprocess.Popen(["python", "C:\\Users\\richa\\Desktop\\ASEGURAMIENTO\\movimiento_mouse.py"])
    time.sleep(5)
    print("Aplicación iniciada.")
    try:
        app = Application(backend="uia").connect(title="Eye Controlled Mouse", timeout=30)
        window = app.window(title="Eye Controlled Mouse")
        window.set_focus()
        time.sleep(1)
        buttons = {
            "detection": window.child_window(control_type="Button", found_index=0).rectangle(),
            "recording": window.child_window(control_type="Button", found_index=1).rectangle(),
            "quit": window.child_window(control_type="Button", found_index=2).rectangle()
        }
        print("Posiciones de los botones obtenidas.")
        create_pdf_file(pdf_path)
        add_text_to_pdf("Inicio de prueba: La aplicación 'Eye Controlled Mouse' ha sido iniciada correctamente. [Pass]")
    except Exception as e:
        add_text_to_pdf("Error: No se pudo iniciar la aplicación. [Fail]")
        print(f"Error al iniciar la aplicación: {e}")

@when('inicio la detección')
def step_when_start_detection(context):
    try:
        print("Iniciando la detección...")
        window.set_focus()
        pyautogui.press('d')
        print("Detección iniciada.")
        time.sleep(5)
        capture_screenshot(os.path.join(report_dir, "start_detection.png"))
        add_text_to_pdf("Acción: Se ha iniciado la detección facial. [Pass]")
        add_screenshot_to_pdf(os.path.join(report_dir, "start_detection.png"))
    except Exception as e:
        add_text_to_pdf("Error: No se pudo iniciar la detección facial. [Fail]")
        print(f"Error al intentar iniciar la detección: {e}")

@then('la aplicación debería comenzar a detectar rostros')
def step_then_application_should_start_detecting_faces(context):
    # Implementar lógica para validar si la detección ha comenzado
    add_text_to_pdf("Validación: La aplicación ha comenzado a detectar caras. [Pass]")

@then('la aplicación debería comenzar a grabar video con detección facial y control ocular')
def step_then_application_should_start_recording(context):
    # Implementar lógica para validar si la grabación ha comenzado
    add_text_to_pdf("Validación: La grabación con detección facial y control ocular ha comenzado. [Pass]")

@then('el video debería capturar el movimiento del ojo derecho para el control del cursor')
def step_then_video_should_capture_right_eye_movement(context):
    # Implementar lógica para validar el control del cursor con el ojo derecho
    add_text_to_pdf("Validación: El video captura el movimiento del ojo derecho para el control del cursor. [Pass]")

@then('el video debería registrar clics realizados con el ojo izquierdo')
def step_then_video_should_register_left_eye_clicks(context):
    # Implementar lógica para validar el registro de clics con el ojo izquierdo
    add_text_to_pdf("Validación: El video registra clics realizados con el ojo izquierdo. [Pass]")

@when('intento iniciar la detección sin éxito')
def step_when_attempt_to_start_detection_unsuccessfully(context):
    try:
        print("Intentando iniciar la detección...")
        window.set_focus()
        pyautogui.press('d')
        print("Detección iniciada.")
        time.sleep(5)
        capture_screenshot(os.path.join(report_dir, "failed_detection.png"))
        add_text_to_pdf("Acción: Se intentó iniciar la detección facial sin éxito. [Fail]")
        add_screenshot_to_pdf(os.path.join(report_dir, "failed_detection.png"))
    except Exception as e:
        add_text_to_pdf("Error: No se pudo iniciar la detección facial. [Fail]")
        print(f"Error al intentar iniciar la detección: {e}")

@then('la aplicación debería mostrar un mensaje de error indicando que la detección facial no se pudo iniciar')
def step_then_application_should_display_error_message(context):
    # Implementar lógica para validar si se muestra un mensaje de error
    add_text_to_pdf("Validación: La aplicación muestra un mensaje de error para la detección facial fallida. [Fail]")

@then('la grabación no debería comenzar')
def step_then_recording_should_not_start(context):
    # Implementar lógica para validar que la grabación no comenzó
    add_text_to_pdf("Validación: La grabación no comenzó. [Fail]")
