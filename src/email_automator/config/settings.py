import os
from pathlib import Path
from dotenv import load_dotenv

# Encontrar el archivo .env
# Esto busca arriba: config -> email_automator -> src -> RAÍZ DEL PROYECTO
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

# 2. Cargar las variables del .env en la memoria de Python
load_dotenv(dotenv_path=ENV_PATH)

class Settings:
    # Clase que valida y almacena la configuración.
    # leer las variables. Si no existen en el .env, serán None.
    EMAIL_SERVER = os.getenv("EMAIL_SERVER", "outlook.office365.com")
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")

    @classmethod
    def validate(cls):
        # Revisa que tengamos usuario y contraseña antes de empezar.
        if not cls.EMAIL_USER or not cls.EMAIL_PASS:
            raise ValueError(
                " --- ERROR DE CONFIGURACIÓN: \n No se encontraron 'EMAIL_USER' o 'EMAIL_PASS'.\n"
                " Por favor, revisa tu archivo .env --- "
            )
        print(f"--- Configuración cargada para: {cls.EMAIL_USER} ---")

settings = Settings()