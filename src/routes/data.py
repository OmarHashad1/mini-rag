from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from configs import get_settings, Settings
from controllers import get_data_controller, DataController, ProcessController
from enums import ResponseEnum, ResponseSignalEnum
from repositories import ProjectRepo, ChunkRepo, AssetRepo
from schemas import ProcessRequest
from models import Chunk, Asset
from enums import AssetEnum
import os
import aiofiles
import logging


data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])
logger = logging.getLogger("uvicorn.error")


project_repo = ProjectRepo()
chunk_repo = ChunkRepo()
asset_repo = AssetRepo()

ALLOWED_MIME_TYPES = {t.value for t in AssetEnum}


@data_router.post("/upload/{project_id}")
async def upload_file(
    project_id: str,
    file: UploadFile,
    app_settings: Settings = Depends(get_settings),
    data_controller: DataController = Depends(get_data_controller),
):
    try:
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=400, detail=f"Unsupported file type: {file.content_type}"
            )

        is_valid, message, signal = data_controller.validate_uplaod_file(file)

        project = await project_repo.insert_or_find_doc(data={"project_id": project_id})

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

        asset = Asset(
            project_id=project.id,
            asset_type=file.content_type,
            asset_name=file_id,
            asset_size=os.path.getsize(file_path),
        )

        await asset_repo.insert_one(data=dict(asset))

        return JSONResponse(
            content={
                "signal": ResponseSignalEnum.FILE_UPLOADED_SUCCESSFULLY.value,
                "message": message,
                "data": {
                    "asset_name": asset.asset_name,
                    "asset_type": asset.asset_type.value,
                    "project_id": asset.project_id.__str__(),
                    "asset_size": asset.asset_size,
                },
            },
            status_code=200,
        )
    except HTTPException as e:
        logging.error(f"Error while uplaoding file: {e}")
        raise
    except Exception as e:
        print(e)
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
        do_reset = dto.do_reset
        process_controller = ProcessController(project_id=project_id)
        file_content = process_controller.get_file_content(file_id=file_id)
        file_chunks = process_controller.process_file_content(
            file_content=file_content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        project = await project_repo.find_one(data={"project_id": project_id})

        if project is None:
            raise HTTPException(
                detail={
                    "signal": ResponseSignalEnum.PROJECT_NOT_FOUND.value,
                    "message": ResponseEnum.PROJECT_NOT_FOUND.value,
                },
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if file_chunks is None or len(file_chunks) == 0:
            raise HTTPException(
                detail={
                    "signal": ResponseSignalEnum.FILE_PROCESSING_FAILED.value,
                    "message": ResponseEnum.FILE_PROCESSING_FAILED.value,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        print(project.id, do_reset)

        chunks_list = [
            dict(
                Chunk(
                    chunk_text=chunk.page_content,
                    chunk_metadata=chunk.metadata,
                    chunk_order=i + 1,
                    chunk_project_id=project.id,
                )
            )
            for i, chunk in enumerate(file_chunks)
        ]
        if do_reset == 1:
            await chunk_repo.delete_many(query={"chunk_project_id": project.id})

        docs_inserted = await chunk_repo.insert_bulk(data=chunks_list)
        return JSONResponse(
            content={
                "signal": ResponseSignalEnum.FILE_PROCESSING_SUCCESS.value,
                "message": ResponseEnum.FILE_PROCESSING_SUCCESS.value,
                "chunks_count": docs_inserted,
            }
        )
    except FileNotFoundError:
        return JSONResponse(
            content={
                "signal": ResponseSignalEnum.FILE_NOT_FOUND.value,
                "message": ResponseEnum.FILE_NOT_FOUND.value,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
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
