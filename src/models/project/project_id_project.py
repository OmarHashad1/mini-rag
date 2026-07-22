from pydantic import BaseModel


class ProjectId(BaseModel):
    project_id: str
