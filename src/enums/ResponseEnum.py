from enum import Enum


class ResponseEnums(Enum):
    FILE_TYPE_NOT_SUPPORTED = (
        "File type is not supported, only PDF and TXT files are supported"
    )
    FILE_SIZE_EXCEEDED = "File must not exceed 10 MB of size"
    FILE_UPLOADED_SUCCESSFULLY = "File uploaded Successfully"
