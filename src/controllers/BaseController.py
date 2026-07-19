from configs import get_settings, Settings
import os
import random
import string


class BaseController:
    def __init__(self):
        self.app_settings: Settings = get_settings()
        self.base_dir = os.path.dirname(
            os.path.dirname(__file__)
        )  # Go from a file, up to its folder, then up one more folder. Return the src the directory path
        self.files_dir = os.path.join(
            self.base_dir, "assets/files"
        )  # concat the base_dir (src) with the assets directory

    def generate_random_string(self, length: int = 12):
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
