from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING
from typing import Annotated
from datetime import datetime, timezone


class Chunk(Document):
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: Annotated[
        PydanticObjectId, Indexed(unique=False, index_type=ASCENDING)
    ]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True

    class Settings:
        name = "chunks"
