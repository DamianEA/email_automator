from email_automator.config.settings import settings
from email_automator.services.pdf_service import PDF_Service
from email_automator.services.email_service import EmailService

def test():
    print("\n\n     Iniciando prueba de Outlook...\n\n")
    
# 1. Validar configuración
    try:
        settings.validate()
    except ValueError as e:
        print(e)
        return

    # 2. Iniciar servicios
    email_botsito = EmailService()
    pdf_botsito = PDF_Service(output_folder="temporal_pdfs") # Carpeta temporal antes de subir a Box

    # 3. Obtener correos (Traemos solo 3 para probar)
    emails = email_botsito.fetch_emails(limit=10)

    if not emails:
        print("\n   No se encontraron correos o hubo error de conexión.\n")
        return

    # 4. Procesar cada correo
    for email in emails:
        print(f" cargando : {email['subject']} ...")
        
        # Generar el PDF con el nombre fecha_asunto
        pdf_path = pdf_botsito.convert_html_to_pdf(email['content'], email['filename'])
        
        # --- AQUÍ IRÁ EL CÓDIGO DE SUBIR A BOX ---
        # box_service.upload(pdf_path)
        # os.remove(pdf_path) # Borrar después de subir
        # -----------------------------------------

    print("--- Ciclo terminado exitosamente.---")

if __name__ == "__main__":
    test()