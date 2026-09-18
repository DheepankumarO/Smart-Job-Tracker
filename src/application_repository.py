from psycopg.rows import dict_row

from database import get_connection


def get_all_applications():
    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    company,
                    position,
                    location,
                    job_url,
                    application_date,
                    status,
                    notes,
                    created_at,
                    updated_at
                FROM applications
                ORDER BY id;
                """
            )

            return cursor.fetchall()

def create_application(
    company,
    position,
    location,
    job_url,
    application_date,
    status,
    notes=None
):
    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                INSERT INTO applications (
                    company,
                    position,
                    location,
                    job_url,
                    application_date,
                    status,
                    notes
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING
                    id,
                    company,
                    position,
                    location,
                    job_url,
                    application_date,
                    status,
                    notes,
                    created_at,
                    updated_at;
                """,
                (
                    company,
                    position,
                    location,
                    job_url,
                    application_date,
                    status,
                    notes
                )
            )

            return cursor.fetchone()

def update_application_status(application_id, new_status):
    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                UPDATE applications
                SET
                    status = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING
                    id,
                    company,
                    position,
                    status,
                    updated_at;
                """,
                (
                    new_status,
                    application_id
                )
            )

            return cursor.fetchone()

def delete_application(application_id):
    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                DELETE FROM applications
                WHERE id = %s
                RETURNING
                    id,
                    company,
                    position;
                """,
                (application_id,)
            )

            return cursor.fetchone()

def update_application_url(application_id, new_url):
    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                UPDATE applications
                SET
                    job_url = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING
                    id,
                    company,
                    job_url,
                    updated_at;
                """,
                (
                    new_url,
                    application_id
                )
            )

            return cursor.fetchone()

def find_applications_by_company(company):
    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    company,
                    position,
                    location,
                    job_url,
                    application_date,
                    status,
                    notes
                FROM applications
                WHERE company ILIKE %s
                ORDER BY id;
                """,
                (f"%{company}%",)
            )

            return cursor.fetchall()

if __name__ == "__main__":
    updated_application = update_application_url(
        3,
        "https://google.com/jobs/intern"
    )

    if updated_application is None:
        print("Application not found.")
    else:
        print("Job URL updated successfully:")
        print(updated_application)
        