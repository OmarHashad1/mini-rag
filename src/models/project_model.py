from pydantic import Field
from beanie import Document


class Project(Document):
    project_id: str = Field(..., min_length=1)

    class Config:
        arbitrary_types_allowed = True

    class Settings:
        name = "projects"

    @classmethod
    def get_indexes(cls):
        pass