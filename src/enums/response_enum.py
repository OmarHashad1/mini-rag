from enum import Enum


class ResponseEnum(Enum):
    FILE_TYPE_NOT_SUPPORTED = (
        "File type is not supported, only PDF and TXT files are supported"
    )
    FILE_SIZE_EXCEEDED = "File must not exceed 10 MB of size"
    FILE_UPLOADED_SUCCESSFULLY = "File uploaded Successfully"
    FILE_UPLOAD_FAILED = "Failed to upload the file"
    FILE_PROCESSING_SUCCESS = "File Processed Successfully"
    FILE_NOT_FOUND = "File not found"
    FILE_PROCESSING_FAILED = "Failed to process the file"
    PROJECT_NOT_FOUND = "Project not found"


class ResponseSignalEnum(Enum):
    FILE_TYPE_NOT_SUPPORTED = "FILE_TYPE_NOT_SUPPORTED"
    FILE_SIZE_EXCEEDED = "FILE_SIZE_EXCEEDED"
    FILE_UPLOADED_SUCCESSFULLY = "FILE_UPLOADED_SUCCESSFULLY"
    FILE_UPLOAD_FAILED = "FILE_UPLOADED_FAILED"
    FILE_PROCESSING_SUCCESS = "FILE_PROCESSED_SUCCESSFULLY"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    FILE_PROCESSING_FAILED = "FILE_PROCESSED_FAILED"
    PROJECT_NOT_FOUND = "PROJECT_NOT_FOUND"
