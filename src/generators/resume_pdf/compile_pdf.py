import subprocess
import tempfile
from pathlib import Path


def compile_latex_to_pdf(latex_code: str, filename: str = "cv") -> Path:
    """
    Compila código LaTeX a PDF en un directorio temporal. Retorna la ruta al archivo PDF generado.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        tex_file = temp_path / f"{filename}.tex"
        pdf_file = temp_path / f"{filename}.pdf"

        tex_file.write_text(latex_code, encoding="utf-8")

        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(temp_path), str(tex_file)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if not pdf_file.exists():
            raise FileNotFoundError("No se generó el PDF.")

        final_pdf = Path(tempfile.gettempdir()) / f"{filename}_final.pdf"
        final_pdf.write_bytes(pdf_file.read_bytes())

        return final_pdf
