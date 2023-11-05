from enum import Enum
from typing import Any

from pydantic import BaseModel

from empire.server.core.db import models


class BadRequestResponse(BaseModel):
    detail: str


class NotFoundResponse(BaseModel):
    detail: str


class ValueType(str, Enum):
    string = "STRING"
    float = "FLOAT"
    integer = "INTEGER"
    boolean = "BOOLEAN"
    file = "FILE"


class CustomOptionSchema(BaseModel):
    description: str
    required: bool
    value: str
    suggested_values: list[str]
    strict: bool
    value_type: ValueType


class OrderDirection(str, Enum):
    asc = "asc"
    desc = "desc"


class DownloadDescription(BaseModel):
    id: int
    filename: str
    link: str

    class Config:
        orm_mode = True


class Author(BaseModel):
    name: str | None
    handle: str | None
    link: str | None


def domain_to_dto_download_description(download: models.Download):
    if download.filename:
        filename = download.filename
    else:
        filename = download.location.split("/")[-1]

    return DownloadDescription(
        id=download.id,
        filename=filename,
        link=f"/api/v2/downloads/{download.id}/download",
    )


def to_value_type(value: Any, type: str = "") -> ValueType:
    type = type or ""
    if type.lower() == "file":
        return ValueType.file
    elif type.lower() in ["string", "str"] or isinstance(value, str):
        return ValueType.string
    elif type.lower() in ["boolean", "bool"] or isinstance(value, bool):
        return ValueType.boolean
    elif type.lower() == "float" or isinstance(value, float):
        return ValueType.float
    elif type.lower() in ["integer", "int"] or isinstance(value, int):
        return ValueType.integer
    else:
        return ValueType.string


# Set proxy IDs
PROXY_NAME = {
    "SOCKS4": 1,
    "SOCKS5": 2,
    "HTTP": 3,
    "SSL": 4,
    "SSL_WEAK": 5,
    "SSL_ANON": 6,
    "TOR": 7,
    "HTTPS": 8,
    "HTTP_CONNECT": 9,
    "HTTPS_CONNECT": 10,
}

# inverse of PROXY_NAME
PROXY_ID = {v: k for k, v in PROXY_NAME.items()}
