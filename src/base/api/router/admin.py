import datetime
import logging

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from ...config import ENV
from ...utils.common import convert_datetime_to_timestamp

router = APIRouter(
    prefix="",
    tags=["Admin APIs"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(ENV.app_name)


@router.get("/restart", status_code=status.HTTP_200_OK)
async def restart():
    watch_file = f"{ENV.base_dir}/timestamp.tmp"
    with open(watch_file, "w", encoding="utf-8") as f:
        f.write(convert_datetime_to_timestamp(datetime.datetime.now()))


@router.get("/config", status_code=status.HTTP_200_OK)
async def setting():
    result = ENV.dict(exclude=ENV.except_vars())
    return JSONResponse(content=result)


@router.get("/ping", status_code=status.HTTP_200_OK)
async def ping(request: Request):
    result = {
        "host": request.client.host,
        "port": request.client.port,
        "timestamp": convert_datetime_to_timestamp(datetime.datetime.now()),
    }
    return JSONResponse(content=result)
