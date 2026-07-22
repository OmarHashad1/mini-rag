from controllers.base_controller import BaseController
from controllers.project_controller import ProjectController
from fastapi import UploadFile
from enums import ResponseEnum, ResponseSignalEnum
import re
import os


class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_uplaod_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.ALLOWED_MIM_TYPES:
            return (
                False,
                ResponseEnum.FILE_TYPE_NOT_SUPPORTED.value,
                ResponseSignalEnum.FILE_TYPE_NOT_SUPPORTED.value,
            )

        if file.size > (self.app_settings.FILE_MAX_SIZE * 1024 * 1024):
            return (
                False,
                ResponseEnum.FILE_SIZE_EXCEEDED.value,
                ResponseSignalEnum.FILE_SIZE_EXCEEDED.value,
            )

        return (
            True,
        )

    def generate_unique_file_name(self, orig_name: str, project_id: str):
        try:
            random_prefix = self.generate_random_string()
            clean_file_name = self.get_clean_file_name(orign_file_name=orig_name)

            unique_file_name = random_prefix + "_" + clean_file_name
            return unique_file_name
        except Exception:
            raise

    def get_file_path(self, orig_name: str, project_id: str):
        try:
            unique_file_name = self.generate_unique_file_name(
                orig_name=orig_name, project_id=project_id
            )
            project_path = ProjectController().get_project_path(project_id=project_id)
            new_file_path = os.path.join(project_path, unique_file_name)
            while os.path.exists(new_file_path):
                unique_file_name = self.generate_unique_file_name(
                    orig_name=orig_name, project_id=project_id
                )
                new_file_path = os.path.join(project_path, unique_file_name)

            return new_file_path, unique_file_name
        except Exception:
            raise

    def get_clean_file_name(self, orign_file_name: str):
        cleaned_file_name = re.sub(r"[^\w.]", "", orign_file_name.strip())
        cleaned_file_name = cleaned_file_name.replace(" ", "_")
        return cleaned_file_name


def get_data_controller():
    return DataController()
