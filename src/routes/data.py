from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from configs import get_settings, Settings
from controllers import get_data_controller, DataController
from enums import ResponseEnums
import aiofiles
import logging

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])
logger = logging.getLogger("uvicorn.error")


@data_router.post("/upload/{project_id}")
async def upload_file(
    project_id: str,
    file: UploadFile,
    app_settings: Settings = Depends(get_settings),
    data_controller: DataController = Depends(get_data_controller),
):
    try:
        is_valid, message = data_controller.validate_uplaod_file(file)

        if not is_valid:
            raise HTTPException(status_code=400, detail=message)

        file_path = data_controller.get_file_path(
            orig_name=file.filename, project_id=project_id
        )

        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUCK_SIZE):
                await f.write(chunk)

        return JSONResponse(content={"message": message}, status_code=200)
    except HTTPException as e:
        logging.error(f"Error while uplaoding file: {e}")
        raise
    except Exception as e:
        logging.error(f"Error while uplaoding file: {e}")
        return JSONResponse(
            content=f"{ResponseEnums.FILE_UPLOAD_FAILED.value}",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
