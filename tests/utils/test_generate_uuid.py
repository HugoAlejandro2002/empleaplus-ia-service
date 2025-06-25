import re
import uuid
from unittest.mock import patch

from src.utils.uuid_generator import generate_uuid


def test_generate_uuid_format():
    uid = generate_uuid()
    assert isinstance(uid, str)
    assert re.fullmatch(
        r"[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}", uid
    )


@patch("src.utils.uuid_generator.uuid.uuid4", return_value=uuid.UUID("12345678-1234-5678-1234-567812345678"))
def test_generate_uuid_mocked(mock_uuid):
    uid = generate_uuid()
    assert uid == "12345678-1234-5678-1234-567812345678"
    mock_uuid.assert_called_once()
