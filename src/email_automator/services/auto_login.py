import time
from playwright.sync_api import Page

class Autologin:
    def __init__(self, page: Page):
        self.page = page

    def login(self, email, password):
        
        print("... Entrando a Outlook...")
        self.page.goto("https://outlook.office.com/mail/PSC@ibm.com/")

        try:
            # Login Microsoft inicial
            self.page.fill('input[type="email"]', email)
            self.page.keyboard.press("Enter")
            
            print("---> Esperando redirección (5 seg)...")
            time.sleep(5)
            
            # Paso Intermedio (Botón w3id Password)
            self._boton()

            # Formulario
            self._login_out(email, password)

            # Esperar Bandeja
            self._esperar()
            
        except Exception as e:
            print(f"### ---> Nota durante login: {e}")
            print("---> Continúa manualmente si es necesario.")
            
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
    def _boton(self):
        # Buscamos el botón específico que mostraste en la captura
        boton_metodo = self.page.locator("text=w3id Password")
        if boton_metodo.count() > 0 and boton_metodo.is_visible():
            boton_metodo.click()
            time.sleep(3) # Esperar a que cargue el siguiente form
        else:
            print("### ----> No vi la pantalla de selección, quizás pasó directo.")
            
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
    def _login_out(self, email, password):
        # Esperamos un momento a que aparezca el campo password
        try:
            self.page.wait_for_selector('input[type="password"]', timeout=5000)
        except:
            pass

        if self.page.locator('input[type="password"]').is_visible():
            # Llenar usuario si falta (a veces se borra)
            try:
                self.page.fill('input[name="username"], input[id="username"]', email)
            except:
                pass 
            
            # Llenar password
            self.page.fill('input[type="password"]', password)
            
            # Checkbox Remember
            try:
                self.page.locator("text=Remember my email address").click()
            except:
                pass

            # Click Sign in
            self.page.click('button:has-text("Sign in"), input[type="submit"]')
            print("---> Credenciales enviadas.")
        else:
            print("### ---> No veo el campo de contraseña, revisa la pantalla.")
            
#//////////////////////////////////////////////////////////////////////////////////////////////////////////
    def _esperar_bandeja(self):
        print("---> Esperando carga de la bandeja (Tienes 2 min para MFA)...")
        self.page.wait_for_selector('div[role="listbox"]', timeout=120000)
        print("---> detectado")