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
            texto = self.page.locator("div.outer div.inner").inner_text()
            
            etiquetas_comunes = ["Today", "Yesterday", "Last week", "Last month", "Older", 
                                "Hoy", "Ayer", "La semana pasada", "El mes pasado"]
            print(self.page.evaluate("document.activeElement.outerHTML"))
            txt_limpio = texto.split('\n')[0].strip() if texto else ""

            if txt_limpio in etiquetas_comunes:
                    return True, self.page.keyboard.press("ArrowDown")
            return False
        except:
            return False