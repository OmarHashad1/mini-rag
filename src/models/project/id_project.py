from pydantic import BaseModel, Field
from beanie import PydanticObjectId


class ID(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
