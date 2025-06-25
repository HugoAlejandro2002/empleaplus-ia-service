from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.dependencies.auth import get_current_user_email
from src.main import app

client = TestClient(app)


@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "password": "secure123",
        "name": "Test User"
    }

@pytest.fixture
def login_data():
    return {
        "email": "test@example.com",
        "password": "secure123"
    }

@pytest.fixture
def reset_data():
    return {
        "oldPassword": "oldpass123",
        "newPassword": "newpass123"
    }


@patch("src.controllers.auth_controller.auth_service.register")
def test_register_user(mock_register, user_data):
    mock_register.return_value = {"message": "User registered"}
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"message": "User registered"}
    mock_register.assert_called_once()


@patch("src.controllers.auth_controller.auth_service.login")
def test_login_user(mock_login, login_data):
    mock_login.return_value = {"access_token": "abc", "refresh_token": "xyz"}
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    assert response.json() == {"access_token": "abc", "refresh_token": "xyz"}
    mock_login.assert_called_once()


@patch("src.controllers.auth_controller.auth_service.reset_password")
def test_reset_password(mock_reset, reset_data):
    mock_reset.return_value = {"message": "Password updated"}
    app.dependency_overrides[get_current_user_email] = lambda: "test@example.com"

    response = client.put("/api/v1/auth/reset-password", json=reset_data)

    assert response.status_code == 200
    assert response.json() == {"message": "Password updated"}
    mock_reset.assert_called_once()

    app.dependency_overrides = {}