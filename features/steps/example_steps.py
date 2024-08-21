from behave import given, when, then
import subprocess
import time
from datetime import datetime
import os

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
current_y = 750
image_height = 300

# Crear un nuevo directorio 'reports' para cada ejecución
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_dir = f"reports_{timestamp}"
os.makedirs(report_dir)

pdf_path = os.path.join(report_dir, f"test_report_{timestamp}.pdf")
c = None

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
    print("Iniciando la aplicación...")
    process = subprocess.Popen(["python", "path_to_your_application.py"])
    time.sleep(5)
    print("Aplicación iniciada.")

    try:
        app = Application(backend="uia").connect(title="Your Application Title", timeout=30)
        window = app.window(title="Your Application Title")
        print("Enfocando la ventana...")
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

@when('I start recording')
def step_when_start_recording(context):
    try:
        print("Intentando hacer clic en el botón de Iniciar Grabación...")
        click(coords=(buttons["recording"].left + 10, buttons["recording"].top + 10))
        print("Hizo clic en el botón de Iniciar Grabación.")
        time.sleep(5)
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
        window.set_focus()
        pyautogui.press('d')
        print("Se presionó la tecla 'D' para iniciar la detección.")
        time.sleep(5)
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
        window.set_focus()
        pyautogui.press('d')
        print("Se presionó la tecla 'D' para detener la detección.")
        time.sleep(5)
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
        time.sleep(5)
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
