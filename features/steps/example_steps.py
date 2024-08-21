"""import os
from datetime import datetime
from behave import given, when, then
import subprocess
import time
import pyautogui
from pywinauto import Application
from pywinauto.mouse import click
from PIL import ImageGrab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
os.makedirs(report_dir)

pdf_path = os.path.join(report_dir, f"test_report_{timestamp}.pdf")
c = None  # Canvas global

def create_pdf_file(file_name):
    global c
    c = canvas.Canvas(file_name, pagesize=letter)
    c.setFont("Helvetica", 12)  # Establecer la fuente correctamente
    print(f"PDF {file_name} creado.")

def capture_screenshot(file_name):
    screenshot = ImageGrab.grab()
    screenshot.save(file_name)
    print(f"Captura de pantalla guardada como {file_name}.")

def add_text_to_pdf(text):
    global c, current_y
    c.drawString(100, current_y, text)
    current_y -= 20  # Ajustar la posición Y para el próximo texto
    if current_y < 50:
        c.showPage()
        current_y = 750

def add_screenshot_to_pdf(image_path):
    global c, current_y
    if current_y < image_height + 50:  # Ajustar si la imagen no cabe en la página actual
        c.showPage()
        current_y = 750
    c.drawImage(image_path, 10, current_y - image_height, 500, image_height)  # Ajusta las coordenadas y tamaño según necesites
    current_y -= image_height + 20  # Ajustar la posición Y para la próxima imagen o texto

def close_pdf():
    global c
    c.save()
    print(f"PDF {pdf_path} cerrado.")

@given('the application is running')
def step_given_application_running(context):
    global process, app, window, buttons
    print("Iniciando la aplicación...")
    process = subprocess.Popen(["python", "C:\\Users\\yanac\\OneDrive\\Escritorio\\DOCUMENTOS DE 6TO SEMESTRE\\APLICACIONES BASADAS EN EL CONOCIMIENTO\\ASEGURAMIENTO\\movimiento_mouse.py"]) 
            
    time.sleep(5)  # Esperar a que la aplicación se inicie
    print("Aplicación iniciada.")

    try:
        app = Application(backend="uia").connect(title="Eye Controlled Mouse", timeout=30)
        window = app.window(title="Eye Controlled Mouse")
        print("Enfocando la ventana...")
        window.set_focus()
        time.sleep(1)  # Esperar para asegurarse de que la ventana esté enfocada

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

@when('I start recording')
def step_when_start_recording(context):
    try:
        print("Intentando hacer clic en el botón de Iniciar Grabación...")
        click(coords=(buttons["recording"].left + 10, buttons["recording"].top + 10))
        print("Hizo clic en el botón de Iniciar Grabación.")
        time.sleep(5)  # Espera para asegurarse de que la grabación ha comenzado
        capture_screenshot(os.path.join(report_dir, "start_recording.png"))
        add_text_to_pdf("Acción: Se ha iniciado la grabación de la cámara. [Pass]")
        add_screenshot_to_pdf(os.path.join(report_dir, "start_recording.png"))
    except Exception as e:
        add_text_to_pdf("Error: No se pudo iniciar la grabación. [Fail]")
        print(f"Error al intentar hacer clic en el botón de Iniciar Grabación: {e}")

@when('I start detection')
def step_when_start_detection(context):
    try:
        print("Intentando iniciar la detección con la tecla 'D'...")
        window.set_focus()  # Asegurarse de que la ventana esté enfocada antes de enviar la tecla
        pyautogui.press('d')
        print("Se presionó la tecla 'D' para iniciar la detección.")
        time.sleep(5)  # Espera para asegurarse de que la detección ha comenzado
        capture_screenshot(os.path.join(report_dir, "start_detection.png"))
        add_text_to_pdf("Acción: Se ha iniciado la detección facial. [Pass]")
        add_screenshot_to_pdf(os.path.join(report_dir, "start_detection.png"))
    except Exception as e:
        add_text_to_pdf("Error: No se pudo iniciar la detección facial. [Fail]")
        print(f"Error al intentar iniciar la detección con la tecla 'D': {e}")

@when('I stop detection')
def step_when_stop_detection(context):
    try:
        print("Intentando detener la detección con la tecla 'D'...")
        window.set_focus()  # Asegurarse de que la ventana esté enfocada antes de enviar la tecla
        pyautogui.press('d')
        print("Se presionó la tecla 'D' para detener la detección.")
        time.sleep(5)  # Espera para asegurarse de que la detección ha terminado
        capture_screenshot(os.path.join(report_dir, "stop_detection.png"))
        add_text_to_pdf("Acción: Se ha detenido la detección facial. [Pass]")
        add_screenshot_to_pdf(os.path.join(report_dir, "stop_detection.png"))
    except Exception as e:
        add_text_to_pdf("Error: No se pudo detener la detección facial. [Fail]")
        print(f"Error al intentar detener la detección con la tecla 'D': {e}")

@then('I stop recording')
def step_then_stop_recording(context):
    try:
        print("Intentando hacer clic en el botón de Detener Grabación...")
        click(coords=(buttons["recording"].left + 10, buttons["recording"].top + 10))
        print("Hizo clic en el botón de Detener Grabación.")
        time.sleep(5)  # Espera para asegurarse de que la grabación ha terminado
        capture_screenshot(os.path.join(report_dir, "stop_recording.png"))
        add_text_to_pdf("Acción: Se ha detenido la grabación de la cámara. [Pass]")
        add_screenshot_to_pdf(os.path.join(report_dir, "stop_recording.png"))
    except Exception as e:
        add_text_to_pdf("Error: No se pudo detener la grabación. [Fail]")
        print(f"Error al intentar hacer clic en el botón de Detener Grabación: {e}")
    finally:
        print("Cerrando la aplicación...")
        process.terminate()
        print("Aplicación cerrada.")
        close_pdf()
"""