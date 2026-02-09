# Outlook Web to PDF Automator

Este robot automatiza la descarga y conversión de correos electrónicos de **Outlook Web** a archivos PDF.

A diferencia de otros scripts, este robot utiliza **Navegación Web Real (Playwright)**, lo que permite:
1.  Saltar bloqueos de seguridad corporativos (MFA/2FA).
2.  No guardar contraseñas (el login es manual y seguro).
3.  Generar PDFs visualmente idénticos al correo original.

## Requisitos Previos

Antes de instalar, asegúrate de tener:
1.  **Python 3.10+**
2.  **Poetry** (Gestor de dependencias).
3.  **GTK3 Runtime** (Indispensable para generar PDFs en Windows).
    * *Descarga:* [GTK-for-Windows-Runtime-Environment-Installer](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
    * *Importante:* Al instalar, marca la casilla **"Set up PATH environment variable"**.

## Instalación

1.  **Clonar/Descargar el proyecto** en tu carpeta.
2.  **Instalar dependencias de Python:**
    ```bash
    poetry install
    ```
3.  **Instalar navegadores del robot:**
    ```bash
    poetry run playwright install chromium
    ```

## Configuración

### Cambiar ruta de descarga
Por defecto, los PDFs se guardan en la carpeta del proyecto. Para cambiarlo:
1.  Abre `src/email_automator/main.py`.
2.  Busca la variable `carpeta_pdfs` al inicio de la función `iniciar_robot`.
3.  Pega la ruta de tu carpeta deseada (ej. `r"C:\Documentos\Auditoria"`).

## Cómo usar

1.  Ejecuta el robot desde la terminal:
    ```bash
    poetry run python src/email_automator/main.py
    ```

2.  **Se abrirá una ventana de navegador.**
    * Ingresa tu correo, contraseña y aprueba el acceso en tu celular (MFA).
    * Espera a que cargue la **Bandeja de Entrada**.

3.  **El robot tomará el control:**
    * Procesará los correos en lotes de 5.
    * Guardará los PDFs automáticamente.
    * En la terminal te preguntará si quieres continuar con los siguientes 5 correos antiguos.
    * Escribe `s` para seguir o `n` para terminar.

## Solución de Problemas

* **Error `OSError: cannot load library 'libgobject-2.0-0'`**:
    * Te falta instalar el GTK3 Runtime (ver Requisitos). Reinicia VS Code después de instalarlo.
* **El navegador no carga o da error de red**:
    * Verifica tu conexión a internet.
    * Si usas VPN corporativa, intenta desconectarla momentáneamente.

---
*Desarrollado para automatización de auditoría de correos.*