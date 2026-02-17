import time
import os
import re
import base64
from pathlib import Path

from datetime import datetime
from playwright.sync_api import Page

# Importamos nuestros nuevos micro-servicios
from email_automator.services.pdf_service import PDF_Service
from email_automator.services.browser import Browser
from email_automator.services.pdf_format import PDF_format
from email_automator.services.capture import Capture


#///////////////////////////////////////////////////////////////////////////////////////////
class Scanner:
    def __init__(self, page: Page, carpeta_salida: str):
        self.page = page
        self.carpeta_salida = carpeta_salida
        
        
        self.browser = Browser(page)
        self.format = PDF_format(page)
        self.capture = Capture(page, carpeta_salida)
        self.pdf_service = PDF_Service()
        

        os.makedirs(self.carpeta_salida, exist_ok=True)

#///////      LIMPIAR NOMBRE          //////////////////////////////////////////////////////////////////
    def cls(self, texto):
        if not texto: return "sin_asunto"
        limpio = re.sub(r'[^\w\s-]', '', texto)
        return limpio.strip().replace(' ', '_')[:50]

#////////         AGREGAR ASUNTO         ///////////////////////////////////////////////////////////////
    def asunto(self):
        try:
            elem = self.page.locator('div[role="heading"][aria-level="2"]').first
            if elem.is_visible():
                return self.cls(elem.inner_text())
        except:
            pass
        return "sin_asunto"

#////////     (LOTE) PROCESO DE AGRUPAR, CONTAR, EJECUTAR    /////////////////////////////////////////////////////////////////
    def lote(self, contador, cantidad=5):
        print(f"\n---> Procesando lote de {cantidad} correos ---\n")
        
        procesados = 0
        

        while procesados < cantidad:
            time.sleep(0.5) 
            
            # VALIDACIÓN: ¿Es encabezado?
            if self.browser.etiqueta():
                print("---> Es un encabezado/grupo. Bajando...")
                self.browser.page.keyboard.press("ArrowDown")
                continue # Reinicia el bucle, no cuenta nada
            # PREPARACIÓN
            print(f"---> ...Procesando correo {contador + 1}...")
            time.sleep(2) # Espera carga
            
            # Limpieza visual (Expandir, quitar basura)
            elemento_a_capturar = self.format.make_format()

            # CAPTURA (Usando TU servicio, no manual)
            # Esto guarda en Documents/PDFs/temp
            ruta_img, ruta_str = self.capture.tomar_foto(elemento_a_capturar, contador)

            # DECISIÓN: ¿Hay foto? -> Hay PDF
            if ruta_img and ruta_img.exists():
                
                # --- A. Generar PDF ---
                asunto_clean = self.asunto()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_pdf = f"{contador+1:03d}_{timestamp}_{asunto_clean}.pdf"
                ruta_pdf = os.path.join(self.carpeta_salida, nombre_pdf)

                ruta_uri = ruta_img.resolve().as_uri()
                
                html = f"""
                <!DOCTYPE html><html><body style="margin:0; padding:0;">
                    <img src="{ruta_uri}" style="width: 100%; display: block;">
                </body></html>
                """

                try:
                    self.pdf_service.html_to_pdf(html, ruta_pdf)
                    print(f"---> PDF Guardado: {nombre_pdf}\n")

                    # Solo aquí contamos y borramos temporal
                    self.capture.limpiar_foto(ruta_str)
                    procesados += 1
                    contador += 1
                    
                    # Avanzamos al siguiente correo
                    self.browser.next()

                except Exception as e:
                    print(f"### ---> Error generando PDF: {e}\n")
                    self.browser.page.keyboard.press("ArrowDown")

            else:
                # --- C. FALLO DE FOTO ---
                print("\n### ---> La captura falló o salió vacía. Saltando...\n")
                self.browser.page.keyboard.press("ArrowDown")

            time.sleep(0.5)

        return contador
    
