import json
import re


def clean_json_output(raw: str) -> dict:
    """
    Limpia la salida de texto que debería ser JSON.
    Elimina encabezados tipo Markdown (```json ... ```) y espacios extra.

    Args:
        raw (str): La cadena cruda devuelta por el agente.

    Returns:
        dict: El objeto JSON parseado.
    """
    cleaned = raw.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"```$", "", cleaned, flags=re.IGNORECASE).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"El JSON del agente no es válido:\n{cleaned}") from e
