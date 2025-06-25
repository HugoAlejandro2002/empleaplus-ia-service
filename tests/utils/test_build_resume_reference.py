import re
from datetime import datetime, timezone
from unittest.mock import patch

from src.utils.resume_reference_builder import (
    build_resume_reference,
    generate_resume_filename,
)


def test_generate_resume_filename_standard():
    full_name = "John Doe"
    date_str = datetime.now().strftime("%Y%m%d")
    filename = generate_resume_filename(full_name)
    assert filename == f"john_doe_resume_{date_str}.pdf"


def test_generate_resume_filename_with_special_chars():
    full_name = "María-José López"
    filename = generate_resume_filename(full_name)
    assert re.match(r"mar_a_resume_\d{8}\.pdf", filename)


def test_generate_resume_filename_with_suffix_and_extension():
    full_name = "Test User"
    filename = generate_resume_filename(full_name, suffix="_v2", extension=".tex")
    date_str = datetime.now().strftime("%Y%m%d")
    assert filename == f"test_user_resume_{date_str}_v2.tex"

@patch("src.utils.resume_reference_builder.generate_resume_filename", return_value="john_doe_resume_20250625.pdf")
@patch("src.utils.resume_reference_builder.datetime")
def test_build_resume_reference(mock_datetime, mock_generate_filename):
    fixed_time = datetime(2025, 6, 25, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = fixed_time

    result = build_resume_reference("resume-123", "John Doe")

    assert result.id == "resume-123"
    assert result.filename == "john_doe_resume_20250625.pdf"
    assert result.created_at == fixed_time.isoformat()
