from imap_tools import MailBox, AND
from datetime import datetime
import re
from email_automator.config.settings import settings

class EmailService:
    def __init__(self):
        self.server = settings.EMAIL_SERVER
        self.user = settings.EMAIL_USER
        self.password = settings.EMAIL_PASS
        # coneccion
    def clean_name(self, subject, date_obj):
        # 1 Formatear la fecha con año-mes-día
        date_str = date_obj.strftime("%Y-%m-%d")
        
        # 2 quitar caracteres prohibidos en Windows como / : * ? " < > |
        clean_subject = re.sub(r'[\\/*?:"<>|]', "", subject)
        
        # 3. Unir y quitar espacios extra
        filename = f"{date_str}_{clean_subject}".strip().replace(" ", "_")
        return filename

    def fetch_emails(self, limit=5):
        # Conecta y trae los últimos 'limit' correos.
        print(f" CONECTANDO A {self.server}...")
        
        emails_data = []
        
        try:
            with MailBox(self.server).login(self.user, self.password) as box:
                # FILTRO, Por ahora traemos todo lo de la bandeja de entrada.
                # Luego podemos filtrar por (no leídos) o 'subject="Factura"'.
                print(" Buscando correos...")
                
                # fetch(criterio, limite, orden descendente por fecha)
                for msg in box.fetch(limit=limit, reverse=True):
                    
                    # Generamos el nombre
                    file_name = self.clean_name(msg.subject, msg.date)
                    
                    # contenido HTML, si no hay, usamos texto
                    content = msg.html if msg.html else f"<pre>{msg.text}</pre>"
                    
                    emails_data.append({
                        "subject": msg.subject,
                        "filename": file_name,
                        "content": content,
                        "date": msg.date
                    })
                    
            print(f"---Se encontraron {len(emails_data)} correos.---")
            return emails_data

        except Exception as e:
            print(f"\n   --- Error conectando a Outlook: {e} ---\n")
            return []