from pydantic import BaseModel


class AssetName(BaseModel):
    asset_name: str
