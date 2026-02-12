import time
from playwright.sync_api import Page

class PDF_format:
    def __init__(self, page: Page):
        self.page = page

#////////    INYECCIONES DE JS Y FORMATO     /////////////////////////////////////////////////
    def make_format(self):
    
        try:

            self.page.click('div[aria-label="Reading Pane"]', timeout=500)
        except:
            pass

        try:
            botones = self.page.locator('button[aria-label="See more"]')
            if botones.count() > 0:
                botones.first.click()
                time.sleep(0.5)
        except:
            pass

        panel = self.page.locator('div[aria-label="Reading Pane"], div[role="document"]').first
        if panel.count() == 0:
            panel = self.page.locator('#app > div').first

        try:
            panel.evaluate("el => { \
                el.style.height = 'auto'; \
                el.style.maxHeight = 'none'; \
                el.style.overflow = 'visible'; \
            }")
            return panel # Retornamos el elemento para que el fotógrafo sepa a qué tomarle foto
        except:
            return None