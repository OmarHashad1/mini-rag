from fastapi import APIRouter, Depends
from configs import get_settings, Settings

base_router = APIRouter(prefix="/api/v1", tags=["api_v1"])


@base_router.get("/")
def index(app_settings: Settings = Depends(get_settings)):
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {"app_nam": app_name, "app_version": app_version}


@base_router.get("/health")
def health():
    return {"message": "ok"}

