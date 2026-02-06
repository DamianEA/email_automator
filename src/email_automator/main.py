import time
import os
import re
from datetime import datetime
from playwright.sync_api import sync_playwright
from email_automator.services.pdf_service import PDF_Service

def clean(texto):
    # Limpia el asunto para usarlo como nombre de archivo
    if not texto:
        return "sin_asunto"
    limpio = re.sub(r'[^\w\s-]', '', texto)
    return limpio.strip().replace(' ', '_')[:50]

def lote(page, servicio_pdf, carpeta_pdfs, contador_global, cantidad=5):
    
    # Procesa un lote de correos y devuelve el contador actualizado.
    
    print(f"\n---> Procesando {cantidad} correos (Iniciando en #{contador_global + 1}) ---")
    
    for i in range(cantidad):
        numero_correo = contador_global + 1 
        
        print(f"\n---> Leyendo correo #{numero_correo}...")
        
        # Intentar obtener el asunto
        asunto = "sin_asunto"
        try:
                                            # Configuracion visual del correo
            elemento_asunto = page.locator('div[role="heading"][aria-level="12"], span[role="heading"]').first
            if elemento_asunto.is_visible():
                asunto = clean(elemento_asunto.inner_text())
        except:
            pass

        # Extraer contenido
        contenido_html = ""
        try:
            # leer solo el panel de lectura
            frame_lectura = page.locator('div[aria-label="Reading Pane"], div[role="document"]')
            if frame_lectura.count() > 0:
                contenido_html = frame_lectura.first.inner_html()
            else:
                contenido_html = page.content()
        except:
            contenido_html = page.content()

        # Generar PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{numero_correo:03d}_{timestamp}_{asunto}.pdf"
        ruta_final = os.path.join(carpeta_pdfs, nombre_archivo)
        
        estilo = "<style>body { background-color: #fff; color: #000; font-family: sans-serif; }</style>"
        try:
            servicio_pdf.html_to_pdf(estilo + contenido_html, ruta_final)
            print(f"---> PDF guardado: {nombre_archivo}")
        except Exception as e:
            print(f"#---> Error guardando PDF: {e}")

        # 4. Bajar al siguiente correo
        if i < cantidad: 
            print("---> Bajando al siguiente correo...")
            page.keyboard.press("ArrowDown")
            time.sleep(2) # Espera breve para cargar
            
        contador_global += 1

    return contador_global

def bridge():
    print("---> INICIANDO PROCESO <---")
    
    # --- RUTA PERSONALIZADA ---
    # Asegúrate de que esta ruta exista o cámbiala por la que gustes
    carpeta_pdfs = r"C:\Users\AngelDamianAvelarZep\Documents\PDFs" 
    
    os.makedirs(carpeta_pdfs, exist_ok=True)
    print(f"---> Los PDFs se guardarán en: {carpeta_pdfs}")

    with sync_playwright() as p:
        # headless=False ES LA CLAVE: Esto hace que se vea la ventana
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print("---> Entrando a Outlook...")
        page.goto("https://outlook.office.com/mail/PSC@ibm.com/")
        
        print("\n" + "="*30)
        print("---> LOGIN MANUAL")
        print("="*30 + "\n")
        
        try:
            # Esperamos hasta 1 minuto a que cargue la lista de correos
            page.wait_for_selector('div[role="listbox"]', timeout=60000)
            print("---> Bandeja detectada.")
        except:
            print("---> No se detectó la bandeja a tiempo.")
            browser.close()
            return

        time.sleep(1)

        # Seleccionar el primer correo
        print("---> Seleccionando correos...")
        try:
            page.click('div[role="listbox"]') 
        except:
            pass
        page.keyboard.press("Home")
        page.keyboard.press("Enter")
        time.sleep(1)

        servicio_pdf = PDF_Service()
        contador_global = 0
        
        while True:
            contador_global = lote(page, servicio_pdf, carpeta_pdfs, contador_global, cantidad=5)
            
            print("\n" + "*"*20)
            print(f"---> Llevamos {contador_global} correos procesados.")
            respuesta = input("---> ¿Procesar los siguientes 5? (s/n): ")
            
            if respuesta.lower() != 's':
                print("### Finalizado. ###")
                break
            
            print("---> Continuando...")
        
        browser.close()

if __name__ == "__main__":
    bridge()