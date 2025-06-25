import io
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.dependencies.auth import get_current_user_email
from src.main import app

client = TestClient(app)

# ---------------- FIXTURES ----------------

@pytest.fixture
def input_cv_request():
    return {
        "personalData": {
            "fullName": "John Doe",
            "email": "john@example.com",
            "phone": "123456789",
            "linkedin": "https://linkedin.com/in/johndoe"
        },
        "education": [],
        "experience": [],
        "skills": [],
        "languages": [],
        "certifications": [],
        "professionalSummary": {
            "summary": "Software engineer with 5 years of experience"
        }
    }

@pytest.fixture
def dummy_resume_data():
    return {
        "fullName": "John Doe",
        "summary": "Software engineer with 5 years of experience",
        "contact": {
            "email": "john@example.com",
            "phone": "123456789",
            "linkedin": "https://linkedin.com/in/johndoe"
        },
        "education": [],
        "experience": [],
        "skills": [],
        "languages": [],
        "certifications": []
    }

@pytest.fixture
def rename_request():
    return {"filename": "new_resume_name"}

# ---------------- TESTS DE RUTAS PROTEGIDAS ----------------

def test_protected_routes_fail_without_auth(input_cv_request, rename_request):
    endpoints_with_body = [
        ("post", "/api/v1/resume/generate", input_cv_request),
        ("post", "/api/v1/resume/download-pdf", input_cv_request),
        ("put", "/api/v1/resume/abc/rename", rename_request),
    ]
    endpoints_no_body = [
        ("get", "/api/v1/resume/"),
        ("get", "/api/v1/resume/abc"),
        ("delete", "/api/v1/resume/abc"),
    ]

    for method, url, payload in endpoints_with_body:
        res = getattr(client, method)(url, json=payload)
        assert res.status_code in [401, 403]

    for method, url in endpoints_no_body:
        res = getattr(client, method)(url)
        assert res.status_code in [401, 403]

# ---------------- ENDPOINTS ----------------

@patch("src.controllers.resume_controller.resume_service.generate_resume")
def test_generate_cv(mock_generate, input_cv_request, dummy_resume_data):
    mock_generate.return_value = dummy_resume_data
    app.dependency_overrides[get_current_user_email] = lambda: "john@example.com"
    res = client.post("/api/v1/resume/generate", json=input_cv_request)
    assert res.status_code == 200
    assert res.json()["fullName"] == "John Doe"
    app.dependency_overrides = {}

class AsyncBytesIO:
    def __init__(self, content: bytes):
        self.file = io.BytesIO(content)

    async def __aenter__(self):
        return self.file

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

@patch("src.controllers.resume_controller.user_service.get_user_by_email")
def test_get_resume_refs(mock_get_user):
    mock_get_user.return_value = MagicMock(cvs=[
        {"id": "abc", "filename": "resume.pdf", "created_at": "2025-01-01"}
    ])
    app.dependency_overrides[get_current_user_email] = lambda: "john@example.com"
    res = client.get("/api/v1/resume/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    app.dependency_overrides = {}

@patch("src.controllers.resume_controller.user_service.get_user_by_email")
def test_get_resume_refs_user_not_found(mock_get_user):
    mock_get_user.return_value = None
    app.dependency_overrides[get_current_user_email] = lambda: "john@example.com"
    res = client.get("/api/v1/resume/")
    assert res.status_code == 404
    app.dependency_overrides = {}

@patch("src.controllers.resume_controller.resume_service.get_resume_by_id")
def test_get_resume_by_id_found(mock_get, dummy_resume_data):
    mock_get.return_value = dummy_resume_data
    app.dependency_overrides[get_current_user_email] = lambda: "john@example.com"
    res = client.get("/api/v1/resume/abc")
    assert res.status_code == 200
    assert res.json()["fullName"] == "John Doe"
    app.dependency_overrides = {}

@patch("src.controllers.resume_controller.resume_service.get_resume_by_id")
def test_get_resume_by_id_not_found(mock_get):
    mock_get.return_value = None
    app.dependency_overrides[get_current_user_email] = lambda: "john@example.com"
    res = client.get("/api/v1/resume/invalid-id")
    assert res.status_code == 404
    app.dependency_overrides = {}

@patch("src.controllers.resume_controller.resume_service.remove_resume_reference")
def test_delete_resume_success(mock_remove):
    mock_remove.return_value = True
    app.dependency_overrides[get_current_user_email] = lambda: "john@example.com"
    res = client.delete("/api/v1/resume/abc")
    assert res.status_code == 200
    app.dependency_overrides = {}

@patch("src.controllers.resume_controller.resume_service.remove_resume_reference")
def test_delete_resume_fail(mock_remove):
    mock_remove.return_value = False
    app.dependency_overrides[get_current_user_email] = lambda: "john@example.com"
    res = client.delete("/api/v1/resume/abc")
    assert res.status_code == 404
    app.dependency_overrides = {}

@patch("src.controllers.resume_controller.resume_service.rename_resume_filename")
def test_rename_resume_success(mock_rename, rename_request):
    mock_rename.return_value = True
    app.dependency_overrides[get_current_user_email] = lambda: "john@example.com"
    res = client.put("/api/v1/resume/abc/rename", json=rename_request)
    assert res.status_code == 200
    app.dependency_overrides = {}

@patch("src.controllers.resume_controller.resume_service.rename_resume_filename")
def test_rename_resume_fail(mock_rename, rename_request):
    mock_rename.return_value = False
    app.dependency_overrides[get_current_user_email] = lambda: "john@example.com"
    res = client.put("/api/v1/resume/abc/rename", json=rename_request)
    assert res.status_code == 404
    app.dependency_overrides = {}
