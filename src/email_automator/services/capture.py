import os
from pathlib import Path
from playwright.sync_api import Locator

class Capture:
    def __init__(self, page, carpeta_temporal):
        self.page = page
        self.carpeta_temporal = carpeta_temporal

#//////////     TOMAR SCREENSHOT     /////////////////////////////////////////////////////////////////
    def tomar_foto(self, elemento: Locator, indice_temp: int):

        carpeta_temporal = Path(r"C:\Users\AngelDamianAvelarZep\Documents\PDFs\temp") 
        carpeta_temporal.mkdir(parents=True, exist_ok=True)
        nombre_temp = f"temp_capture_{indice_temp}.png"

        ruta_imagen = carpeta_temporal / nombre_temp
        ruta_str = str(ruta_imagen.resolve())

        try:
            # Intento 1 Foto al elemento específico
            if elemento:
                elemento.screenshot(path=ruta_str, type='png', animations="disabled")
            else:
                raise Exception("Elemento nulo")
        except Exception:
            # Intento 2 Foto a toda la pantalla
            try:
                self.page.screenshot(path=ruta_str, full_page=True, type='png')
            except:
                return None, None

        return ruta_imagen, ruta_str

#//////////     VACIAR CARPETA TERMPORAL     /////////////////////////////////////////////////////////////////
    def limpiar_foto(self, ruta_str):
        try:
            if ruta_str and os.path.exists(ruta_str):
                os.remove(ruta_str)
            else:
                pass
        except Exception as e:
            print(f"### ---> Error limpiando foto temporal: {e}")            