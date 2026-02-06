from weasyprint import HTML

class PDF_Service:
    
    def html_to_pdf(self, html_content, full_path):
        
       # Recibe el contenido HTML y la ruta COMPLETA donde se guardará.
        try:
            print(f"      ⚙️ Guardando en: {full_path}")
            
            # Convierte y guarda directamente en la ruta que nos dio el main
            HTML(string=html_content).write_pdf(target=full_path)
            
            return True
            
        except Exception as e:
            print(f"      ⚠️ Error crítico en PDF Service: {e}")
            raise e