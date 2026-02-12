import time
import os
import re

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
                return self._limpiar_nombre(elem.inner_text())
        except:
            pass
        return "sin_asunto"

#////////     (LOTE) PROCESO DE AGRUPAR, CONTAR, EJECUTAR    /////////////////////////////////////////////////////////////////
    def lote(self, contador, cantidad=5):
        print(f"\n---> Procesando lote de {cantidad} correos (Modo Preciso) ---")
        
        procesados = 0
        
        # Usamos un while true protegido para navegar la cantidad solicitada
        while procesados < cantidad:
            time.sleep(0.5) # Pequeña pausa para que JS reaccione

            # PASO 2: ¿Es una etiqueta?
            if self.browser.etiqueta(): 
                continue # Reinicia el ciclo sin contar este como correo procesado

            # Si llegamos aquí, ES UN CORREO REAL
            numero_correo = contador + 1
            print(f"---> Procesando correo #{numero_correo}...")

            time.sleep(1)

#///////////////////////////////////////////////////////////////////////////////////////////
            # Limpieza Visual
            elemento_a_capturar = self.format.make_format()

            # PASO 5: Captura
            ruta_img, ruta_str = self.capture.tomar_foto(elemento_a_capturar, procesados)

            # PASO 6: Generación de PDF
            exito = False
            if ruta_img and ruta_img.exists():
                asunto = self.asunto()
                
                # Crear HTML
                ruta_uri = ruta_img.resolve().as_uri()
                html = f"""
                <!DOCTYPE html><html><head><style>
                    @page {{ size: A4; margin: 0; }}
                    body {{ margin: 0; padding: 0; }}
                    img {{ width: 100%; height: auto; display: block; }}
                </style></head><body><img src="{ruta_uri}"></body></html>
                """

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nombre_pdf = f"{numero_correo:03d}_{timestamp}_{asunto}.pdf"
                ruta_pdf = os.path.join(self.carpeta_salida, nombre_pdf)

                try:
                    self.pdf_service.html_to_pdf(html, ruta_pdf)
                    print(f"---> PDF Guardado: {nombre_pdf}")
                    exito = True
                except Exception as e:
                    print(f"---> Error guardando PDF: {e}")

                self.capture.limpiar_foto(ruta_str)
            else:
                print("---> La captura salió vacía o falló.")

            # PASO 7: Bajar al siguiente (Solo si procesamos un correo)
            self.browser.next()
            
            # Actualizamos contadores
            procesados += 1
            contador += 1

        return contador
    
