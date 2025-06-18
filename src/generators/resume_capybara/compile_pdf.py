import subprocess
import tempfile
from pathlib import Path


def compile_latex_to_pdf(latex_code: str, filename: str = "cv") -> Path:
    """
    Compila código LaTeX a PDF en un directorio temporal. Retorna la ruta al archivo PDF generado.
    Si hay un error de compilación, imprime stderr y lanza una excepción.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        tex_file  = temp_path / f"{filename}.tex"
        pdf_file  = temp_path / f"{filename}.pdf"
        log_file  = temp_path / f"{filename}.log"

        # 1) Inyectamos en el preámbulo la definición Unicode para U+202F
        #    antes de \begin{document}
        injection = "\n\\DeclareUnicodeCharacter{202F}{ }\n"
        if "\\begin{document}" in latex_code:
            latex_code = latex_code.replace(
                "\\begin{document}",
                injection + "\\begin{document}"
            )
        else:
            # si tu template no usa exactamente esa línea, puedes
            # simplemente anteponerla:
            latex_code = injection + latex_code

        tex_file.write_text(latex_code, encoding="utf-8")

        # 2) Ejecutamos pdflatex sin capturar stdout (el PDF va directo a disco)
        result = subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                "-output-directory", str(temp_path),
                str(tex_file)
            ],
            stdout=subprocess.DEVNULL,   # descartamos la salida binaria
            stderr=subprocess.PIPE,      # capturamos sólo errores/texto
            text=True                    # stderr como string
        )

        # Mostrar sólo stderr
        print("===== pdflatex STDERR =====")
        print(result.stderr)

        if result.returncode != 0 or not pdf_file.exists():
            # Si hay .log, lo mostramos para depuración
            if log_file.exists():
                print("===== pdflatex LOG FILE =====")
                print(log_file.read_text(encoding="utf-8", errors="ignore"))
            raise RuntimeError("La compilación de LaTeX falló. Revisa el log anterior para más detalles.")

        # 3) Mover el PDF a un destino persistente
        final_pdf = Path(tempfile.gettempdir()) / f"{filename}_final.pdf"
        final_pdf.write_bytes(pdf_file.read_bytes())

        return final_pdf
