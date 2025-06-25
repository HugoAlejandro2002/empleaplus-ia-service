import pytest

from src.utils import clean_json_output


def test_clean_valid_json_no_wrapping():
    raw = '{"key": "value", "number": 123}'
    result = clean_json_output(raw)
    assert result == {"key": "value", "number": 123}


def test_clean_json_with_triple_backticks():
    raw = """
    ```json
    {
        "key": "value",
        "items": [1, 2, 3]
    }
    ```
    """
    result = clean_json_output(raw)
    assert result == {"key": "value", "items": [1, 2, 3]}


def test_clean_json_with_backticks_without_json_keyword():
    raw = """
    ```
    {
        "status": "ok"
    }
    ```
    """
    result = clean_json_output(raw)
    assert result == {"status": "ok"}


def test_clean_json_with_extra_whitespace():
    raw = "   \n```json\n{ \"a\": 1 }\n```   "
    result = clean_json_output(raw)
    assert result == {"a": 1}


def test_invalid_json_raises_value_error():
    invalid_raw = """
    ```json
    { invalid json }
    ```
    """
    with pytest.raises(ValueError) as exc:
        clean_json_output(invalid_raw)

    assert "El JSON del agente no es válido" in str(exc.value)
