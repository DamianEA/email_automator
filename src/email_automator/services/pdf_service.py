import os
from pathlib import Path
from weasyprint import HTML

class PDF_Service:
    
    def __init__(self, output_folder: str = "Downloads"):
        # Define la ruta donde se guardarán los archivos.
        self.output_folder = Path.cwd() / output_folder
        
        # Crea la carpeta si no existe.
        if not self.output_folder.exists():
            self.output_folder.mkdir(parents=True, exist_ok=True)
            print(f"Carpeta creada: {self.output_folder}")

    def html_to_pdf(self, html_content: str, file_name: str) -> str:
        #convierte html a pdf.
        try:
            # Asegurar que el nombre termine en .pdf
            if not file_name.endswith('.pdf'):
                file_name += '.pdf'
            
            full_path = self.output_folder / file_name
            
            print(f"cargando... '{file_name}'...")
            
            HTML(string=html_content).write_pdf(target=full_path)
            
            print(f"Hecho! {full_path}")
            return str(full_path)

        except Exception as e:
            print(f"Error generando PDF: {e}")
            raise e