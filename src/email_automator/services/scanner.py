import time
import os
import re
from datetime import datetime
from playwright.sync_api import Page
from email_automator.services.pdf_service import PDF_Service

class Scanner:
    def __init__(self, page: Page, carpeta_salida: str):
        self.page = page
        self.carpeta_salida = carpeta_salida
        self.pdf_service = PDF_Service() # Instancia el servicio aquí
        
        # Asegurar que existe la carpeta de destino
        os.makedirs(self.carpeta_salida, exist_ok=True)
        
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
    def cls(self, texto):
        if not texto:
            return "sin_asunto"
        # Elimina caracteres raros
        limpio = re.sub(r'[^\w\s-]', '', texto)
        return limpio.strip().replace(' ', '_')[:50]
    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
    def lote(self, contador, cantidad=5):
        print(f"\n---> Procesando #{cantidad} correos ---")
        
        for i in range(cantidad):
            num_email = contador + 1
            print(f"---> Leyendo correo #{num_email}...")
            
            # Obtener Asunto
            asunto = "sin_asunto"
            try:
                elem = self.page.locator('div[role="heading"][aria-level="2"], span[role="heading"]').first
                if elem.is_visible():
                    asunto = self.cls(elem.inner_text())
            except:
                pass

            # Obtener HTML
            contenido = ""
            try:
                # Intenta tomar solo el panel de lectura
                frame = self.page.locator('div[aria-label="Reading Pane"], div[role="document"]')
                contenido = frame.first.inner_html() if frame.count() > 0 else self.page.content()
            except:
                contenido = self.page.content()

            # Construir la ruta y Guardar
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"{num_email:03d}_{timestamp}_{asunto}.pdf"
            ruta_final = os.path.join(self.carpeta_salida, nombre_archivo)
            
            estilo = "<style>body { background-color: #fff; color: #000; font-family: sans-serif; }</style>"
            
            try:
                self.pdf_service.html_to_pdf(estilo + contenido, ruta_final)
                print(f" ---> PDF guardado: {nombre_archivo}")
            except Exception as e:
                print(f" ### ---> Error guardando PDF: {e}")

            # Navegar al siguiente
            if i < cantidad:
                self.siguiente()
            
            contador += 1

        return contador
    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
    def siguiente(self):
        try:
            # Click para enfocar el cuerpo antes de bajar
            self.page.click('body', position={'x': 100, 'y': 100})
        except:
            pass
        self.page.keyboard.press("ArrowDown")
        print("\n---> siguiente correo \n")
        time.sleep(2) # Pausa técnica para que cargue el correo