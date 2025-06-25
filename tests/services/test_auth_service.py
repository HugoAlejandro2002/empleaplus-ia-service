from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from src.models import (
    UserDB,
    UserLoginRequest,
    UserRegisterRequest,
    UserResetPasswordRequest,
)
from src.services import AuthService


@pytest.fixture
def auth_service_mocked_repo():
    with patch("src.services.auth_service.UsersRepository") as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo
        yield AuthService(), mock_repo


@patch("src.services.auth_service.hash_password")
def test_register_user_success(mock_hash_password, auth_service_mocked_repo):
    service, mock_repo = auth_service_mocked_repo
    mock_repo.get_user_by_email.return_value = None
    mock_hash_password.return_value = "hashed_password"

    request = UserRegisterRequest(email="test@example.com", password="123456")
    result = service.register(request)

    assert result == {"message": "User registered successfully"}
    mock_repo.insert_user.assert_called_once()
    mock_hash_password.assert_called_once_with("123456")


@patch("src.services.auth_service.hash_password")
def test_register_user_already_exists(mock_hash_password, auth_service_mocked_repo):
    service, mock_repo = auth_service_mocked_repo
    mock_repo.get_user_by_email.return_value = UserDB(email="test@example.com", password="pwd", cvs=[])

    request = UserRegisterRequest(email="test@example.com", password="123456")
    with pytest.raises(HTTPException) as exc:
        service.register(request)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Email already registered"
    mock_repo.insert_user.assert_not_called()


@patch("src.services.auth_service.create_access_token")
@patch("src.services.auth_service.verify_password")
def test_login_success(mock_verify_password, mock_create_token, auth_service_mocked_repo):
    service, mock_repo = auth_service_mocked_repo
    mock_repo.get_user_by_email.return_value = UserDB(email="test@example.com", password="hashedpwd", cvs=[])
    mock_verify_password.return_value = True
    mock_create_token.return_value = "access-token"

    request = UserLoginRequest(email="test@example.com", password="123456")
    result = service.login(request)

    assert result == {"access_token": "access-token", "token_type": "bearer"}
    mock_create_token.assert_called_once()


@patch("src.services.auth_service.verify_password")
def test_login_invalid_password(mock_verify_password, auth_service_mocked_repo):
    service, mock_repo = auth_service_mocked_repo
    mock_repo.get_user_by_email.return_value = UserDB(email="test@example.com", password="wronghash", cvs=[])
    mock_verify_password.return_value = False

    request = UserLoginRequest(email="test@example.com", password="wrongpass")
    with pytest.raises(HTTPException) as exc:
        service.login(request)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid credentials"


def test_login_user_not_found(auth_service_mocked_repo):
    service, mock_repo = auth_service_mocked_repo
    mock_repo.get_user_by_email.return_value = None

    request = UserLoginRequest(email="notfound@example.com", password="123456")
    with pytest.raises(HTTPException) as exc:
        service.login(request)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid credentials"


@patch("src.services.auth_service.hash_password")
@patch("src.services.auth_service.verify_password")
def test_reset_password_success(mock_verify_password, mock_hash_password, auth_service_mocked_repo):
    service, mock_repo = auth_service_mocked_repo
    mock_repo.get_user_by_email.return_value = UserDB(email="test@example.com", password="hashedpwd", cvs=[])
    mock_verify_password.return_value = True
    mock_hash_password.return_value = "newhashedpwd"

    request = UserResetPasswordRequest(oldPassword="123456", newPassword="654321")
    result = service.reset_password(request, email="test@example.com")

    assert result == {"message": "Password updated successfully"}
    mock_repo.update_user_password.assert_called_once_with("test@example.com", "newhashedpwd")


@patch("src.services.auth_service.verify_password")
def test_reset_password_user_not_found(mock_verify_password, auth_service_mocked_repo):
    service, mock_repo = auth_service_mocked_repo
    mock_repo.get_user_by_email.return_value = None

    request = UserResetPasswordRequest(oldPassword="123456", newPassword="654321")
    with pytest.raises(HTTPException) as exc:
        service.reset_password(request, email="notfound@example.com")

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"
