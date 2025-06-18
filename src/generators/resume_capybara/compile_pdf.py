import subprocess
import tempfile
from pathlib import Path


def compile_latex_to_pdf(latex_code: str, filename: str = "cv") -> Path:
    """
    Compila código LaTeX a PDF en un directorio temporal.
    Retorna la ruta al archivo PDF generado.
    Si hay un error de compilación, imprime stderr y lanza una excepción.
    """
    # 0) Sanitizar caracteres invisibles que LaTeX no entiende:
    for bad, good in [
        ("\u200B", ""),   # zero‐width space
        ("\u202F", " "),  # narrow no-break → espacio normal
        ("\u00A0", " "),  # no-break space → espacio
    ]:
        latex_code = latex_code.replace(bad, good)

    # 1) Inyectar en el preámbulo las declaraciones (por si faltasen)
    decls = "\n\\DeclareUnicodeCharacter{202F}{\\,}\n"
    if "\\begin{document}" in latex_code:
        latex_code = latex_code.replace(
            "\\begin{document}",
            decls + "\\begin{document}"
        )
    else:
        latex_code = decls + latex_code

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        tex_file = temp_path / f"{filename}.tex"
        pdf_file = temp_path / f"{filename}.pdf"
        log_file = temp_path / f"{filename}.log"

        tex_file.write_text(latex_code, encoding="utf-8")

        # 2) Ejecutar pdflatex
        result = subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                "-output-directory", str(temp_path),
                str(tex_file)
            ],
            stdout=subprocess.DEVNULL,   # no queremos el volcado binario
            stderr=subprocess.PIPE,      # sí capturamos errores
            text=True                    # stderr → str
        )

        # Mostrar sólo stderr para depuración
        print("===== pdflatex STDERR =====")
        print(result.stderr)

        if result.returncode != 0 or not pdf_file.exists():
            if log_file.exists():
                print("===== pdflatex LOG FILE =====")
                print(log_file.read_text(encoding="utf-8", errors="ignore"))
            raise RuntimeError(
                "La compilación de LaTeX falló. "
                "Revisa el stderr/log anteriores para más detalles."
            )

        # 3) Mover el PDF a un destino persistente
        final_pdf = Path(tempfile.gettempdir()) / f"{filename}_final.pdf"
        final_pdf.write_bytes(pdf_file.read_bytes())
        return final_pdf
