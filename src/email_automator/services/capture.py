import os
from pathlib import Path
from playwright.sync_api import Locator

class Capture:
    def __init__(self, page, carpeta_salida):
        self.page = page
        self.carpeta_salida = carpeta_salida

#//////////     TOMAR SCREENSHOT     /////////////////////////////////////////////////////////////////
    def tomar_foto(self, elemento: Locator, indice_temp: int):
    
        nombre_temp = f"temp_capture_{indice_temp}.png"
        ruta_imagen = Path(self.carpeta_salida) / nombre_temp
        ruta_imagen_str = str(ruta_imagen.resolve())

        try:
            # Intento 1 Foto al elemento específico
            if elemento:
                elemento.screenshot(path=ruta_imagen_str, type='png', animations="disabled")
            else:
                raise Exception("Elemento nulo")
        except Exception:
            # Intento 2 Foto a toda la pantalla
            try:
                self.page.screenshot(path=ruta_imagen_str, full_page=True, type='png')
            except:
                return None, None

        return ruta_imagen, ruta_imagen_str

#//////////     VACIAR CARPETA TERMPORAL     /////////////////////////////////////////////////////////////////
    def limpiar_foto(self, ruta_str):
        try:
            if os.path.exists(ruta_str):
                os.remove(ruta_str)
        except:
            pass
            