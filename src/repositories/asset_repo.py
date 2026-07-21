from .base_repo import BaseRepo
from models import Asset


class AssetRepo(BaseRepo):
    def __init__(self):
        super().__init__(Asset)
