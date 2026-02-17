import time
from playwright.sync_api import Page

class Browser:
    def __init__(self, page: Page):
        self.page = page

#///////////////////////////////////////////////////////////////////////////////////////////
    def _click(self):
        try:
            self.page.evaluate("if(document.activeElement) { document.activeElement.click(); }")
        except:
            pass

#///////////////////////////////////////////////////////////////////////////////////////////////
    def next(self):
        
        try:
            self.page.locator('div[role="listbox"]').focus()
            self.page.keyboard.press("ArrowDown")
            time.sleep(1)
        except:
            # Fallback si falla el foco
            self.page.keyboard.press("ArrowDown")
            time.sleep(1)

#///////////////////////////////////////////////////////////////////////////////////////////////
    def etiqueta(self): # Salta las etiquetas de la barra de correos      
        try:
            # Estrategia combinada (Tu idea del <i> + atributos de seguridad)
            es_tag = self.page.evaluate("""() => {
                const el = document.activeElement;
                if (!el) return false;
                
                // 1: Buscar la etiqueta <i> (ícono chevron) dentro del div
                const tieneIconoColapso = el.querySelector('i[data-icon-name*="Chevron"]') !== null;
                
                // 2: Los headers tienen aria-expanded (true/false)
                const esDesplegable = el.getAttribute('aria-expanded') !== null;
                
                // 3: Los headers suelen ser botones
                const esBoton = el.getAttribute('role') === 'button';
                return tieneIconoColapso || esDesplegable || esBoton;
            }""")
            
            return es_tag
        except Exception as e:
            print(f"Error validando elemento: {e}")
            return False