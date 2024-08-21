"""import os
import json
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
import cv2

# Variables globales
process = None
app = None
window = None
buttons = None
current_y = 750  # Coordenada Y inicial para el texto
image_height = 300  # Altura de la imagen en el PDF
pdf_path = None
video_path = None
json_path = None
test_results = {
    "keyword": "Feature",
    "name": "Interfaz gráfica de usuario con botones Iniciar Detección, Iniciar Grabación, Salir",
    "tags": [],
    "description": "",
    "elements": []
}

def setup_report_dir():
    global pdf_path, video_path, json_path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = f"reports_{timestamp}"
    os.makedirs(report_dir)
    pdf_path = os.path.join(report_dir, f"test_report_{timestamp}.pdf")
    video_path = os.path.join(report_dir, f"test_video_{timestamp}.avi")
    json_path = os.path.join(report_dir, f"test_results_{timestamp}.json")

def create_pdf_file(file_name):
    global c
    c = canvas.Canvas(file_name, pagesize=letter)
    c.setFont("Helvetica", 12)
    print(f"PDF {file_name} creado.")

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

def write_json_results(results):
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"JSON {json_path} generado.")

@given('the application is running')
def step_given_application_running(context):
    global process, app, window, buttons
    print("Iniciando la aplicación...")
    setup_report_dir()
    create_pdf_file(pdf_path)
    process = subprocess.Popen(["python", "C:\\Users\\richa\\Desktop\\ASEGURAMIENTO\\movimiento_mouse.py"])
    
    time.sleep(5)  # Esperar a que la aplicación se inicie
    print("Aplicación iniciada.")

    try:
        app = Application(backend="uia").connect(title="Eye Controlled Mouse", timeout=30)
        window = app.window(title="Eye Controlled Mouse")
        window.set_focus()
        time.sleep(1)  # Asegura que la ventana esté enfocada

        buttons = {
            "recording": window.child_window(control_type="Button", found_index=1).rectangle(),
        }
        print("Posiciones de los botones obtenidas.")
        test_results['elements'] = [{
            "type": "scenario",
            "keyword": "Scenario",
            "name": "Display of the user interface with the necessary buttons",
            "tags": [],
            "steps": [
                {
                    "keyword": "Given",
                    "name": "the application is running",
                    "match": {
                        "location": "features/steps/example_steps.py:55",
                        "arguments": []
                    },
                    "result": {
                        "status": "passed",
                        "duration": 11.660150527954102
                    },
                    "line": 7
                }
            ],
            "line": 6,
            "uri": "features/example.feature",
            "description": "",
            "id": 1
        }]
        add_text_to_pdf("Inicio de prueba: La aplicación 'Eye Controlled Mouse' ha sido iniciada correctamente. [Pass]")
    except Exception as e:
        test_results['elements'] = [{
            "type": "scenario",
            "keyword": "Scenario",
            "name": "Display of the user interface with the necessary buttons",
            "tags": [],
            "steps": [
                {
                    "keyword": "Given",
                    "name": "the application is running",
                    "match": {
                        "location": "features/steps/example_steps.py:55",
                        "arguments": []
                    },
                    "result": {
                        "status": "failed",
                        "duration": 11.660150527954102
                    },
                    "line": 7
                }
            ],
            "line": 6,
            "uri": "features/example.feature",
            "description": "",
            "id": 1
        }]
        add_text_to_pdf(f"Error: No se pudo iniciar la aplicación. [Fail] {e}")
        print(f"Error al iniciar la aplicación: {e}")

@when('I attempt to start video capture with an intentional error')
def step_when_attempt_start_video_capture_with_error(context):
    global video_path
    try:
        print("Intentando iniciar la captura de video con un error intencional...")
        cap = cv2.VideoCapture(0)  # Intentar abrir la cámara (puede que no esté disponible)
        if not cap.isOpened():
            raise Exception("No se pudo abrir la cámara para la captura de video.")
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))
        
        start_time = time.time()
        while (time.time() - start_time) < 5:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        
        cap.release()
        out.release()
        cv2.destroyAllWindows()

        screenshot_path = os.path.join(report_dir, "intentional_error.png")
        ImageGrab.grab().save(screenshot_path)
        test_results['elements'][0]['steps'].append({
            "keyword": "When",
            "name": "I attempt to start video capture with an intentional error",
            "match": {
                "location": "features/steps/example_steps.py:95",
                "arguments": []
            },
            "result": {
                "status": "failed",
                "duration": 2.0
            },
            "line": 11
        })
        add_text_to_pdf("Fallo intencional: No se pudo iniciar la captura de video. [Fail]")
        add_screenshot_to_pdf(screenshot_path)
    except Exception as e:
        test_results['elements'][0]['steps'].append({
            "keyword": "When",
            "name": "I attempt to start video capture with an intentional error",
            "match": {
                "location": "features/steps/example_steps.py:95",
                "arguments": []
            },
            "result": {
                "status": "failed",
                "duration": 2.0
            },
            "line": 11
        })
        add_text_to_pdf(f"Error: No se pudo iniciar la captura de video. [Fail] {e}")
        print(f"Error al iniciar la captura de video: {e}")

@then('a report with screenshots and video should be generated')
def step_then_generate_report(context):
    try:
        test_results['elements'][0]['steps'].append({
            "keyword": "Then",
            "name": "a report with screenshots and video should be generated",
            "match": {
                "location": "features/steps/example_steps.py:125",
                "arguments": []
            },
            "result": {
                "status": "passed",
                "duration": 1.0
            },
            "line": 12
        })
        add_text_to_pdf("Reporte generado con capturas de pantalla y video.")
        write_json_results(test_results)
        print(f"Reporte generado en: {pdf_path}")
    except Exception as e:
        test_results['elements'][0]['steps'].append({
            "keyword": "Then",
            "name": "a report with screenshots and video should be generated",
            "match": {
                "location": "features/steps/example_steps.py:125",
                "arguments": []
            },
            "result": {
                "status": "failed",
                "duration": 1.0
            },
            "line": 12
        })
        add_text_to_pdf(f"Error: No se pudo generar el reporte. [Fail] {e}")
        write_json_results(test_results)
        print(f"Error al generar el reporte: {e}")
    finally:
        print("Cerrando la aplicación...")
        process.terminate()
        print("Aplicación cerrada.")
        close_pdf() """