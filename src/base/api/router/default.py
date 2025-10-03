import logging
import datetime
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from base.utils.common import convert_datetime_to_timestamp
from base.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/app",
    tags=["Default"],
    responses={404: {"description": "Not found"}},
)


@router.get("/restart", status_code=status.HTTP_200_OK)
async def restart():
    watch_file = f"{settings.app.root}/timestamp.tmp"
    with open(watch_file, "w", encoding="utf-8") as f:
        f.write(convert_datetime_to_timestamp(datetime.datetime.now()))


@router.get("/config", status_code=status.HTTP_200_OK)
async def setting():
    config = settings.app.model_dump_json(indent=2)
    return JSONResponse(content=config)


@router.get("/ping", status_code=status.HTTP_200_OK)
async def ping(request: Request):
    result = {
        "host": request.client.host,
        "port": request.client.port,
        "timestamp": convert_datetime_to_timestamp(datetime.datetime.now()),
    }
    return JSONResponse(content=result)
