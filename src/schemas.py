from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


ApplicationStatus = Literal[
    "Saved",
    "Applied",
    "Interview",
    "Offer",
    "Rejected",
    "Withdrawn",
]


class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=150)
    position: str = Field(min_length=1, max_length=150)
    location: str = Field(min_length=1, max_length=150)
    job_url: str | None = None
    application_date: date
    status: ApplicationStatus = "Saved"
    notes: str | None = None
    
class ApplicationUpdate(BaseModel):
    company: str = Field(min_length=1, max_length=150)
    position: str = Field(min_length=1, max_length=150)
    location: str = Field(min_length=1, max_length=150)
    job_url: str | None = None
    application_date: date
    status: ApplicationStatus = "Saved"
    notes: str | None = None
    
class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus