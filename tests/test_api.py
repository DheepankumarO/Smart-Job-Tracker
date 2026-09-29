from fastapi.testclient import TestClient

from src.api import app


client = TestClient(app)

def create_test_application():
    response = client.post(
        "/applications",
        json={
            "company": "Test Company",
            "position": "Python Developer",
            "location": "Remote",
            "job_url": "https://example.com/jobs/python-developer",
            "application_date": "2026-09-29",
            "status": "Applied",
            "notes": "Created during an API test",
        },
    )

    assert response.status_code == 201
    return response.json()

def test_get_application_by_id(clean_test_database):
    created_application = create_test_application()
    application_id = created_application["id"]

    response = client.get(f"/applications/{application_id}")

    assert response.status_code == 200
    assert response.json()["id"] == application_id
    assert response.json()["company"] == "Test Company"

    missing_response = client.get("/applications/999999")

    assert missing_response.status_code == 404
    assert missing_response.json() == {
        "detail": "Application not found"
    }


def test_update_application_status(clean_test_database):
    created_application = create_test_application()
    application_id = created_application["id"]

    response = client.patch(
        f"/applications/{application_id}/status",
        json={"status": "Interview"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Interview"

    invalid_response = client.patch(
        f"/applications/{application_id}/status",
        json={"status": "Waiting"},
    )

    assert invalid_response.status_code == 422


def test_delete_application(clean_test_database):
    created_application = create_test_application()
    application_id = created_application["id"]

    delete_response = client.delete(
        f"/applications/{application_id}"
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["application"]["id"] == application_id

    get_response = client.get(
        f"/applications/{application_id}"
    )

    assert get_response.status_code == 404

    second_delete_response = client.delete(
        f"/applications/{application_id}"
    )

    assert second_delete_response.status_code == 404


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "Smart Job Tracker API is running",
    }


def test_create_and_list_applications(clean_test_database):
    application_data = {
        "company": "Test Company",
        "position": "Python Developer",
        "location": "Remote",
        "job_url": "https://example.com/jobs/python-developer",
        "application_date": "2026-09-29",
        "status": "Applied",
        "notes": "Created during an API test",
    }

    create_response = client.post(
        "/applications",
        json=application_data,
    )

    assert create_response.status_code == 201

    created_application = create_response.json()

    assert created_application["id"] == 1
    assert created_application["company"] == "Test Company"
    assert created_application["status"] == "Applied"

    list_response = client.get("/applications")

    assert list_response.status_code == 200

    applications = list_response.json()

    assert len(applications) == 1
    assert applications[0]["id"] == created_application["id"]