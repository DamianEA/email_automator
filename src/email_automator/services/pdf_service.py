import os
from pathlib import Path
from weasyprint import HTML

class PDF_Service:
    
    def html_to_pdf(self, html_content: str, output_path: str) -> str:
        #convierte html a pdf.
        try:
            # Asegurar que el nombre termine en .pdf
            if not output_path.endswith('.pdf'):
                output_path += '.pdf'
            
            HTML(string=html_content).write_pdf(target=output_path)
            
            print(f"Hecho! {output_path}")
            return str(output_path)

        except Exception as e:
            print(f"Error generando PDF: {e}")
            raise e