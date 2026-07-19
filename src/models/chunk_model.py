from beanie import Document
from pydantic import Field
from bson.objectid import ObjectId


class Chunk(Document):
    text_chunk: str = Field(..., min_length=1)
    metadata: dict
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: ObjectId

    class Config:
        arbitrary_types_allowed=True
    class Settings:
        name = "chunks"
