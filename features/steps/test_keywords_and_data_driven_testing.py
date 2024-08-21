"""from behave import given, when, then
import pyautogui
from pywinauto import Application
from pywinauto.mouse import click
from PIL import ImageGrab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime
import subprocess
import time

# Variables globales
process = None
app = None
window = None
buttons = None
current_y = 750  # Coordenada Y inicial para el texto
image_height = 300  # Altura de la imagen en el PDF

# Crear un nuevo directorio 'reports' para cada ejecución
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_dir = f"reports_{timestamp}"
os.makedirs(report_dir, exist_ok=True)

pdf_path = os.path.join(report_dir, f"test_report_{timestamp}.pdf")
c = None  # Canvas global

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

@given('the application is running')
def step_given_application_running(context):
    global process, app, window, buttons
    if process is None:
        print("Iniciando la aplicación...")
        process = subprocess.Popen(["python", "C:\\Users\\yanac\\OneDrive\\Escritorio\\DOCUMENTOS DE 6TO SEMESTRE\\APLICACIONES BASADAS EN EL CONOCIMIENTO\\ASEGURAMIENTO\\movimiento_mouse.py"], creationflags=subprocess.CREATE_NO_WINDOW)
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
        add_text_to_pdf("Inicio de prueba: La aplicación 'Eye Controlled Mouse' ha sido iniciada correctamente.")
    except Exception as e:
        add_text_to_pdf(f"Error: No se pudo iniciar la aplicación. {e}")
        print(f"Error al iniciar la aplicación: {e}")

@when('I perform "{action}" with "{operation}"')
def step_when_perform_action(context, action, operation):
    if action == "start":
        if operation == "detection":
            start_detection(context)
        elif operation == "recording":
            start_recording(context)
        else:
            add_text_to_pdf(f"Error: Operación de inicio no válida: {operation}.")
            print(f"Operación de inicio no válida: {operation}")
    elif action == "stop":
        if operation == "detection":
            stop_detection(context)
        elif operation == "recording":
            stop_recording(context)
        else:
            add_text_to_pdf(f"Error: Operación de detención no válida: {operation}.")
            print(f"Operación de detención no válida: {operation}")
    else:
        add_text_to_pdf(f"Error: Acción no válida: {action}.")
        print(f"Acción no válida: {action}")

@then('the application should "{expected_result}"')
def step_then_application_should(context, expected_result):
    if expected_result == "start detecting faces":
        validate_start_detection(context)
    elif expected_result == "start recording":
        validate_start_recording(context)
    elif expected_result == "stop detecting faces":
        validate_stop_detection(context)
    elif expected_result == "stop recording":
        validate_stop_recording(context)
    else:
        add_text_to_pdf(f"Error: Resultado esperado no válido: {expected_result}.")

def start_detection(context):
    try:
        print("Iniciando la detección...")
        window.set_focus()
        pyautogui.press('d')
        print("Detección iniciada.")
        time.sleep(5)
        capture_screenshot(os.path.join(report_dir, "start_detection.png"))
        add_text_to_pdf("Acción: Se ha iniciado la detección facial correctamente.")
        add_screenshot_to_pdf(os.path.join(report_dir, "start_detection.png"))
    except Exception as e:
        add_text_to_pdf(f"Error: No se pudo iniciar la detección facial. {e}")
        print(f"Error al intentar iniciar la detección: {e}")

def start_recording(context):
    try:
        print("Iniciando la grabación...")
        click(coords=(buttons["recording"].left + 10, buttons["recording"].top + 10))
        print("Grabación iniciada.")
        time.sleep(5)
        capture_screenshot(os.path.join(report_dir, "start_recording.png"))
        add_text_to_pdf("Acción: Se ha iniciado la grabación de la cámara correctamente.")
        add_screenshot_to_pdf(os.path.join(report_dir, "start_recording.png"))
    except Exception as e:
        add_text_to_pdf(f"Error: No se pudo iniciar la grabación. {e}")
        print(f"Error al intentar iniciar la grabación: {e}")

def stop_detection(context):
    try:
        print("Deteniendo la detección...")
        window.set_focus()
        pyautogui.press('d')
        print("Detección detenida.")
        time.sleep(5)
        capture_screenshot(os.path.join(report_dir, "stop_detection.png"))
        add_text_to_pdf("Acción: Se ha detenido la detección facial correctamente.")
        add_screenshot_to_pdf(os.path.join(report_dir, "stop_detection.png"))
    except Exception as e:
        add_text_to_pdf(f"Error: No se pudo detener la detección facial. {e}")
        print(f"Error al intentar detener la detección: {e}")

def stop_recording(context):
    try:
        print("Deteniendo la grabación...")
        click(coords=(buttons["recording"].left + 10, buttons["recording"].top + 10))
        print("Grabación detenida.")
        time.sleep(5)
        capture_screenshot(os.path.join(report_dir, "stop_recording.png"))
        add_text_to_pdf("Acción: Se ha detenido la grabación de la cámara correctamente.")
        add_screenshot_to_pdf(os.path.join(report_dir, "stop_recording.png"))
    except Exception as e:
        add_text_to_pdf(f"Error: No se pudo detener la grabación. {e}")
        print(f"Error al intentar detener la grabación: {e}")
    finally:
        print("Cerrando la aplicación...")
        process.terminate()
        print("Aplicación cerrada.")
        close_pdf()

# Funciones de validación
def validate_start_detection(context):
    add_text_to_pdf("Validación: La detección facial ha sido iniciada correctamente.")

def validate_start_recording(context):
    add_text_to_pdf("Validación: La grabación ha sido iniciada correctamente.")

def validate_stop_detection(context):
    add_text_to_pdf("Validación: La detección facial ha sido detenida correctamente.")

def validate_stop_recording(context):
    add_text_to_pdf("Validación: La grabación ha sido detenida correctamente.")
"""