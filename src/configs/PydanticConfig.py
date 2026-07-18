from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPENAPI_API_KEY: str
    ALLOWED_MIM_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUCK_SIZE: int

    class Config:
        env_file = "../.env"


def get_settings():
    return Settings()
