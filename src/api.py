from fastapi import FastAPI, HTTPException

from src.application_repository import (
    create_application,
    delete_application,
    get_all_applications,
    get_application_by_id,
    update_application_status,
)
from src.schemas import (
    ApplicationCreate,
    ApplicationStatusUpdate,
)


app = FastAPI(
    title="Smart Job Tracker API",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Smart Job Tracker API is running",
    }


@app.get("/applications")
def list_applications():
    applications = get_all_applications()
    return applications

@app.get("/applications/{application_id}")
def get_application(application_id: int):
    application = get_application_by_id(application_id)

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return application

@app.post("/applications", status_code=201)
def add_application(application: ApplicationCreate):
    created_application = create_application(
        application.company,
        application.position,
        application.location,
        application.job_url,
        application.application_date,
        application.status,
        application.notes,
    )

    return created_application

@app.patch("/applications/{application_id}/status")
def change_application_status(
    application_id: int,
    status_update: ApplicationStatusUpdate,
):
    updated_application = update_application_status(
        application_id,
        status_update.status,
    )

    if updated_application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return updated_application

@app.delete("/applications/{application_id}")
def remove_application(application_id: int):
    deleted_application = delete_application(application_id)

    if deleted_application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return {
        "message": "Application deleted successfully",
        "application": deleted_application,
    }