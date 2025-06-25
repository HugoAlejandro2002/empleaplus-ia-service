from unittest.mock import MagicMock, patch

import pytest

from src.models import ResumeReference, UserDB
from src.repositories import UsersRepository


@pytest.fixture
def users_repository():
    with patch("src.repositories.user_repository.get_users_table") as mock_get_table:
        mock_table = MagicMock()
        mock_get_table.return_value = mock_table
        repo = UsersRepository()
        return repo, mock_table


def test_insert_user(users_repository):
    repo, table = users_repository
    user = UserDB(email="test@example.com", password="pwd", cvs=[])
    repo.insert_user(user)
    table.put_item.assert_called_once_with(Item=user.model_dump())


def test_get_user_by_email_found(users_repository):
    repo, table = users_repository
    user_dict = {"email": "test@example.com", "password": "pwd", "cvs": []}
    table.get_item.return_value = {"Item": user_dict}

    user = repo.get_user_by_email("test@example.com")

    assert isinstance(user, UserDB)
    assert user.email == "test@example.com"


def test_get_user_by_email_not_found(users_repository):
    repo, table = users_repository
    table.get_item.return_value = {}
    user = repo.get_user_by_email("test@example.com")
    assert user is None


def test_append_resume_entry(users_repository):
    repo, table = users_repository
    resume = ResumeReference(id="cv1", filename="cv1.pdf", created_at="2024-01-01")

    repo.append_resume_entry("test@example.com", resume)

    table.update_item.assert_called_once_with(
        Key={"email": "test@example.com"},
        UpdateExpression="SET cvs = list_append(if_not_exists(cvs, :empty_list), :entry)",
        ExpressionAttributeValues={
            ":entry": [resume.model_dump()],
            ":empty_list": []
        }
    )


def test_remove_resume_reference_success(users_repository):
    repo, table = users_repository
    repo.get_user_by_email = MagicMock(return_value=UserDB(
        email="test@example.com", password="pwd", cvs=[
            ResumeReference(id="a", filename="cv1", created_at="2024-01-01"),
            ResumeReference(id="b", filename="cv2", created_at="2024-01-01")
        ]
    ))

    result = repo.remove_resume_reference("test@example.com", "a")
    assert result is True
    table.update_item.assert_called_once()


def test_remove_resume_reference_user_not_found(users_repository):
    repo, table = users_repository
    repo.get_user_by_email = MagicMock(return_value=None)

    result = repo.remove_resume_reference("test@example.com", "cv1")
    assert result is False
    table.update_item.assert_not_called()


def test_rename_resume_filename_success(users_repository):
    repo, table = users_repository
    user = UserDB(
        email="test@example.com", password="pwd",
        cvs=[ResumeReference(id="cv1", filename="old", created_at="2024-01-01")]
    )
    repo.get_user_by_email = MagicMock(return_value=user)

    result = repo.rename_resume_filename("test@example.com", "cv1", "new")
    assert result is True
    assert user.cvs[0].filename == "new"
    table.update_item.assert_called_once()


def test_rename_resume_filename_not_found(users_repository):
    repo, table = users_repository
    user = UserDB(
        email="test@example.com", password="pwd",
        cvs=[ResumeReference(id="cv1", filename="old", created_at="2024-01-01")]
    )
    repo.get_user_by_email = MagicMock(return_value=user)

    result = repo.rename_resume_filename("test@example.com", "cvX", "new")
    assert result is False
    table.update_item.assert_not_called()


def test_update_user_password(users_repository):
    repo, table = users_repository
    repo.update_user_password("test@example.com", "new-hash")

    table.update_item.assert_called_once_with(
        Key={"email": "test@example.com"},
        UpdateExpression="SET password = :p",
        ExpressionAttributeValues={":p": "new-hash"}
    )