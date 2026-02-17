import os
import time

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from email_automator.services.auto_login import Autologin
from email_automator.services.scanner import Scanner
from pathlib import Path

load_dotenv()

def process():
    print("---> INICIANDO <---")
    
    # Credenciales y Configuración
    email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    
    # CAMBIA LA RUTA
    carpeta_pdfs = Path(r"C:\Users\AngelDamianAvelarZep\Documents\PDFs")

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

        # Ir al inicio tiempo de espera
        time.sleep(3)

        try:
            # Buscamos la lista de correos (listbox) y dentro, la primera opción
            lista_correos = page.locator('div[role="listbox"]')
            primer_correo = lista_correos.locator('div[role="option"]').first
            
            # Forzamos la espera hasta que aparezca
            primer_correo.wait_for(timeout=3000)
            time.sleep(1)
        except:
            time.sleep(1)

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