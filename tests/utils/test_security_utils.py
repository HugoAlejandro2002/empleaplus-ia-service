import pytest
from fastapi import HTTPException
from jose import jwt

from src.core import get_settings
from src.utils.security import (
    create_access_token,
    credentials_exception,
    decode_token,
    hash_password,
    verify_password,
)

settings = get_settings()
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.jwt_hash_algorithm


def test_hash_and_verify_password():
    raw_password = "securePassword123!"
    hashed = hash_password(raw_password)
    
    assert isinstance(hashed, str)
    assert hashed != raw_password
    assert verify_password(raw_password, hashed)
    assert not verify_password("wrongPassword", hashed)


def test_create_access_token_and_decode_token():
    payload = {"sub": "test@example.com"}
    token = create_access_token(payload, expires_minutes=5)

    assert isinstance(token, str)
    
    decoded_email = decode_token(token)
    assert decoded_email == "test@example.com"


def test_decode_token_invalid_signature():
    invalid_token = jwt.encode({"sub": "test@example.com"}, "wrong_key", algorithm=ALGORITHM)
    
    with pytest.raises(HTTPException) as exc:
        decode_token(invalid_token)
    
    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid or expired token"


def test_decode_token_missing_sub():
    token = jwt.encode({"foo": "bar"}, SECRET_KEY, algorithm=ALGORITHM)
    
    with pytest.raises(HTTPException) as exc:
        decode_token(token)
    
    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid or expired token"


def test_credentials_exception_raises_http_exception():
    with pytest.raises(HTTPException) as exc:
        raise credentials_exception()

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid or expired token"
