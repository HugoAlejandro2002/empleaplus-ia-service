import subprocess
import tempfile
from pathlib import Path


def compile_latex_to_pdf(latex_code: str, filename: str = "cv") -> Path:
    """
    Compila código LaTeX a PDF en un directorio temporal. Retorna la ruta al archivo PDF generado.
    Si hay un error de compilación, imprime stdout/stderr y lanza una excepción.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        tex_file = temp_path / f"{filename}.tex"
        pdf_file = temp_path / f"{filename}.pdf"
        log_file = temp_path / f"{filename}.log"

        tex_file.write_text(latex_code, encoding="utf-8")

        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode",
            "-output-directory", str(temp_path),
            str(tex_file)],
            stdout=subprocess.DEVNULL,       # descartamos la salida binaria
            stderr=subprocess.PIPE,          # capturamos sólo errores/texto
            text=True                        # stderr vendrá como str, no bytes
        )

        # Mostrar salida de pdflatex
        print("===== pdflatex STDOUT =====")
        print(result.stdout)
        print("===== pdflatex STDERR =====")
        print(result.stderr)

        if result.returncode != 0 or not pdf_file.exists():
            # Guardar log si existe
            if log_file.exists():
                print("===== pdflatex LOG FILE =====")
                print(log_file.read_text(encoding="utf-8"))

            raise RuntimeError("La compilación de LaTeX falló. Revisa el log anterior para más detalles.")

        # Mover a un path final reutilizable
        final_pdf = Path(tempfile.gettempdir()) / f"{filename}_final.pdf"
        final_pdf.write_bytes(pdf_file.read_bytes())

        return final_pdf
