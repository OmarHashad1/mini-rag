from typing import Annotated
from pydantic import Field
from beanie import Document, Indexed
from pymongo import ASCENDING
from datetime import datetime, timezone


class Project(Document):
    project_id: Annotated[str, Indexed(unique=True, index_type=ASCENDING)] = Field(
        ..., min_length=1
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True

    class Settings:
        name = "projects"
