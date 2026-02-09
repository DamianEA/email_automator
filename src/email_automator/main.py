import os
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from email_automator.services.auto_login import Autologin
from email_automator.services.scanner import Scanner

# Cargar configuración
load_dotenv()

def process():
    print("---> INICIANDO <---")
    
    # Credenciales y Configuración
    email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    
    # Aquí pon tu ruta de escritorio
    carpeta_pdfs = r"C:\Users\angel\Documents\PDFs"

    if not email or not password:
        print("### ---> ERROR: Faltan credenciales en .env")
        return

    with sync_playwright() as p:
        # Abrir Navegador
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Iniciar
        auth = Autologin(page)
        scanner = Scanner(page, carpeta_pdfs)

        # Ejecutar Login
        auth.login(email, password)

        # Preparar Interfaz (Ir al inicio)
        time.sleep(2)
        page.keyboard.press("Home")
        time.sleep(2)

        # Bucle Principal de Trabajo
        contador = 0
        while True:
            contador = scanner.lote(contador, cantidad=5)
            
            print(f"\n---> Total procesado: {contador}")
            res = input("\n---> ¿Seguir con el siguiente lote? (s/n): ").lower()
            if res != 's':
                break
        
        print("\n... FINALIZADO ...")
        browser.close()

if __name__ == "__main__":
    process()