from fastapi import APIRouter, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
from configs import get_settings, Settings
from controllers import DataController
from controllers import ProjectController
import os
import aiofiles

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])


@data_router.post("/upload/{project_id}")
async def upload_file(
    project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)
):
    try:
        is_valid, message = DataController().validate_uplaod_file(file)

        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
        project_dir_path = ProjectController().get_project_path(project_id=project_id)
        file_path = os.path.join(project_dir_path, file.filename)

        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUCK_SIZE):
                await f.write(chunk)
        return JSONResponse(content={"message": message}, status_code=200)
    except HTTPException:
        raise
    except Exception as e:
        return e
