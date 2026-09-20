import os

import pytest

from src.database import get_connection


@pytest.fixture
def clean_test_database(monkeypatch):
    monkeypatch.setenv("DB_NAME", "smart_job_tracker_test")

    if os.getenv("DB_NAME") != "smart_job_tracker_test":
        raise RuntimeError("Tests must use smart_job_tracker_test")

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "TRUNCATE TABLE applications RESTART IDENTITY"
            )

    yield

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "TRUNCATE TABLE applications RESTART IDENTITY"
            )