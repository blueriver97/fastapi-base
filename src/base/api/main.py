import logging
import os
import signal
import traceback
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ..config import ENV
from ..core.fallback_processor import fallback_processor
from ..core.init import Initializer
from ..models.auth import UserOutput
from ..models.exception import Fallback
from ..models.type import FallbackType
from ..utils.auth import get_current_active_user

logger = logging.getLogger(ENV.app_name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_event()
    yield
    await shutdown_event()


async def startup_event():
    try:
        Initializer()()  # Call the Initializer directly
        logger.info(f"STARTUP {ENV.app_name.upper()} HTTP SERVER")
    except Exception as e:
        handle_exception(e, FallbackType.INIT_FAIL)


async def shutdown_event():
    try:
        # Perform any necessary cleanup here
        logger.info(f"SHUTDOWN {ENV.app_name.upper()} HTTP SERVER")
    except Exception as e:
        handle_exception(e, FallbackType.FINAL_FAIL)


def handle_exception(exception: Exception, fallback_type: FallbackType):
    if not isinstance(exception, Fallback):
        exception = Fallback(type=fallback_type, traceback=traceback.format_exc())
    fallback_processor(fallback=exception)
    os.kill(os.getppid(), signal.SIGTERM)
    os.kill(os.getpid(), signal.SIGTERM)


app = FastAPI(lifespan=lifespan)
app.templates = Jinja2Templates(directory=f"{ENV.base_dir}/api/templates")
app.mount("/static", StaticFiles(directory=f"{ENV.base_dir}/api/static"), name="static")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, current_user: UserOutput = Depends(get_current_active_user)):
    logger.debug(current_user)
    return app.templates.TemplateResponse("index.html", context={"request": request})
