from .base_repo import BaseRepo
from models import Project


class ProjectRepo(BaseRepo):
    def __init__(self):
        super().__init__(Project)
