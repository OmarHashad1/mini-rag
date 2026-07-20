from .base_repo import BaseRepo
from models import Chunk


class ChunkRepo(BaseRepo):
    def __init__(self):
        super().__init__(Chunk)
