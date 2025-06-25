from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.generators.resume_pdf.compile_pdf import compile_latex_to_pdf


@patch("src.generators.resume_pdf.compile_pdf.subprocess.run")
@patch("pathlib.Path.write_text")
@patch("pathlib.Path.read_bytes", return_value=b"%PDF-content")
@patch("pathlib.Path.exists", return_value=True)
@patch("tempfile.TemporaryDirectory")
def test_compile_latex_to_pdf_success(mock_tempdir, mock_exists, mock_read_bytes, mock_write_text, mock_run):
    mock_tempdir.return_value.__enter__.return_value = str(Path("/tmp/mockdir"))

    mock_run.return_value = MagicMock(returncode=0, stdout="OK", stderr="")

    result = compile_latex_to_pdf(r"\documentclass{article}\begin{document}Hola Mundo\end{document}")

    assert isinstance(result, Path)
    assert result.name.endswith("_final.pdf")
    mock_run.assert_called_once()


@patch("src.generators.resume_pdf.compile_pdf.tempfile.TemporaryDirectory")
@patch("src.generators.resume_pdf.compile_pdf.subprocess.run")
def test_compile_latex_to_pdf_failure(mock_run, mock_tempdir):
    mock_dir = MagicMock()
    mock_dir.__enter__.return_value = "/tmp/testfail"
    mock_tempdir.return_value = mock_dir

    with patch("pathlib.Path.write_text"), \
         patch("pathlib.Path.exists", return_value=False):
        
        mock_run.return_value = MagicMock(returncode=1, stdout="error", stderr="error")

        with pytest.raises(RuntimeError, match="La compilación de LaTeX falló"):
            compile_latex_to_pdf("bad latex")