from datetime import datetime, timezone
from typing import Annotated, Optional
from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field
from pymongo import ASCENDING, IndexModel

from enums import AssetEnum


class Asset(Document):
    project_id: Annotated[PydanticObjectId, Indexed(unique=False, index_type=ASCENDING)]
    asset_type: AssetEnum
    asset_name: Annotated[str, Indexed(unique=False, index_type=ASCENDING)] = Field(
        ..., min_length=1
    )
    asset_size: Optional[int] = Field(ge=0, default=None)
    asset_config: Optional[dict] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "assets"
        indexes = [
            IndexModel(
                [("project_id", ASCENDING), ("asset_name", ASCENDING)],
                unique=True,
                name="project_id_asset_name_index_1",
            ),
        ]

    class Config:
        arbitrary_types_allowed = True
