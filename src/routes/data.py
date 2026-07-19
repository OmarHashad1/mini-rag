from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from configs import get_settings, Settings
from controllers import get_data_controller, DataController, ProcessController
from enums import ResponseEnum, ResponseSignalEnum
from schemas import ProcessRequest
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
        is_valid, message, signal = data_controller.validate_uplaod_file(file)

        if not is_valid:
            raise HTTPException(
                status_code=400, detail={"signal": signal, "message": message}
            )

        file_path, file_id = data_controller.get_file_path(
            orig_name=file.filename, project_id=project_id
        )

        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUCK_SIZE):
                await f.write(chunk)

        return JSONResponse(
            content={
                "signal": ResponseSignalEnum.FILE_UPLOADED_SUCCESSFULLY.value,
                "message": message,
                "file_id": file_id,
            },
            status_code=200,
        )
    except HTTPException as e:
        logging.error(f"Error while uplaoding file: {e}")
        raise
    except Exception as e:
        logging.error(f"Error while uplaoding file: {e}")
        return JSONResponse(
            content={
                "signal": ResponseSignalEnum.FILE_UPLOAD_FAILED.value,
                "message": ResponseEnum.FILE_UPLOAD_FAILED.value,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@data_router.post("/process/{project_id}")
async def process_file(project_id: str, dto: ProcessRequest):
    try:
        file_id = dto.file_id
        chunk_size = dto.chunk_size
        chunk_overlap = dto.chunk_overlap
        process_controller = ProcessController(project_id=project_id)
        file_content = process_controller.get_file_content(file_id=file_id)
        file_chunks = process_controller.process_file_content(
            file_content=file_content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        if file_chunks is None or len(file_chunks) == 0:
            raise HTTPException(
                detail={
                    "signal": ResponseSignalEnum.FILE_PROCESSING_FAILED.value,
                    "message": ResponseEnum.FILE_PROCESSING_FAILED.value,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return JSONResponse(
            content={
                "signal": ResponseSignalEnum.FILE_PROCESSING_SUCCESS.value,
                "message": ResponseEnum.FILE_PROCESSING_SUCCESS.value,
                "chunks": file_chunks,
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error while uplaoding file: {e}")
        return JSONResponse(
            content={
                "signal": ResponseSignalEnum.FILE_PROCESSING_FAILED.value,
                "message": ResponseEnum.FILE_PROCESSING_FAILED.value,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
