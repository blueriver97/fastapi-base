import logging
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from base.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/app",
    tags=["Default"],
    responses={404: {"description": "Not found"}},
)


@router.get("/config", status_code=status.HTTP_200_OK)
async def setting(request: Request):
    config = settings.app.model_dump_json(indent=2)
    return JSONResponse(content=config)
