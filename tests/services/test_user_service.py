from unittest.mock import MagicMock, patch

import pytest

from src.models import UserDB
from src.services import UserService


@pytest.fixture
def user_repo_mock():
    with patch("src.services.user_service.UsersRepository") as mock_repo_class:
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo
        yield mock_repo


@pytest.fixture
def user_service(user_repo_mock):
    return UserService(), user_repo_mock


def test_get_user_by_email_found(user_service):
    service, mock_repo = user_service

    mock_user = UserDB(email="test@example.com", password="hashed_pwd", cvs=[])
    mock_repo.get_user_by_email.return_value = mock_user

    result = service.get_user_by_email("test@example.com")

    assert result == mock_user
    mock_repo.get_user_by_email.assert_called_once_with("test@example.com")


def test_get_user_by_email_not_found(user_service):
    service, mock_repo = user_service

    mock_repo.get_user_by_email.return_value = None

    result = service.get_user_by_email("nonexistent@example.com")

    assert result is None
    mock_repo.get_user_by_email.assert_called_once_with("nonexistent@example.com")
