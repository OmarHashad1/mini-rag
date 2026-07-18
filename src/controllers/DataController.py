from controllers.BaseController import BaseController
from fastapi import UploadFile
from enums import ResponseEnums


class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_uplaod_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.ALLOWED_MIM_TYPES:
            return (
                False,
                ResponseEnums.FILE_TYPE_NOT_SUPPORTED.value,
            )

        if file.size > (self.app_settings.FILE_MAX_SIZE * 1024 * 1024):
            return False, ResponseEnums.FILE_SIZE_EXCEEDED.value

        return True, ResponseEnums.FILE_UPLOADED_SUCCESSFULLY.value

    def generate_unique_file_name(self, orig_name: str, project_id: str):
        random_file_name = self.generate_random_string()
        return random_file_name
