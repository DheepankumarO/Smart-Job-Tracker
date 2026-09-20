from datetime import date

from src.application_repository import (
    create_application,
    get_all_applications,
    find_applications_by_company,
    update_application_status,
    delete_application,
)


def test_create_and_get_application(clean_test_database):
    created_application = create_application(
        "Test Company",
        "Python Developer",
        "Remote",
        "https://example.com/jobs/1",
        date(2026, 9, 20),
        "Applied",
        "Created by pytest",
    )

    assert created_application["id"] == 1
    assert created_application["company"] == "Test Company"
    assert created_application["status"] == "Applied"

    applications = get_all_applications()

    assert len(applications) == 1
    assert applications[0]["id"] == created_application["id"]
    assert applications[0]["company"] == "Test Company"
    
def test_find_applications_by_company(clean_test_database):
    create_application(
        "TechCorp",
        "Software Engineer",
        "New York",
        "https://techcorp.com/jobs/1",
        date(2026, 9, 20),
        "Applied",
        "Backend position",
    )

    create_application(
        "DataWorks",
        "Data Engineer",
        "Remote",
        "https://dataworks.com/jobs/1",
        date(2026, 9, 20),
        "Saved",
        "Data position",
    )

    results = find_applications_by_company("tech")

    assert len(results) == 1
    assert results[0]["company"] == "TechCorp"
    
def test_update_application_status(clean_test_database):
    created_application = create_application(
        "TechCorp",
        "Software Engineer",
        "New York",
        "https://techcorp.com/jobs/1",
        date(2026, 9, 20),
        "Applied",
        "Waiting for a response",
    )

    updated_application = update_application_status(
        created_application["id"],
        "Interview",
    )

    assert updated_application is not None
    assert updated_application["id"] == created_application["id"]
    assert updated_application["status"] == "Interview"

    applications = get_all_applications()

    assert len(applications) == 1
    assert applications[0]["status"] == "Interview"
    
def test_delete_application(clean_test_database):
    created_application = create_application(
        "Delete Test Company",
        "Test Engineer",
        "Remote",
        "https://example.com/jobs/delete-test",
        date(2026, 9, 20),
        "Saved",
        "This record should be deleted",
    )

    deleted_application = delete_application(
        created_application["id"]
    )

    assert deleted_application is not None
    assert deleted_application["id"] == created_application["id"]
    assert deleted_application["company"] == "Delete Test Company"

    applications = get_all_applications()

    assert applications == []