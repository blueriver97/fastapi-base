import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from base.api.router.auth import router as auth_router
from base.api.router.default import router as default_router

logger = logging.getLogger(__file__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    startup_event()
    yield
    shutdown_event()


def startup_event():
    try:
        # await database.connect()
        logger.info("STARTUP HTTP SERVER")
    except Exception as e:
        raise RuntimeError(f"Failed to start server: {e}")


def shutdown_event():
    try:
        # await database.disconnect()
        logger.info("SHUTDOWN HTTP SERVER")
    except Exception as e:
        raise RuntimeError(f"Failed to shutdown server: {e}")


app = FastAPI(lifespan=lifespan)

template_dir = Path(__file__).parent / "templates"
static_dir = Path(__file__).parent / "static"

app.templates = Jinja2Templates(directory=template_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

app.include_router(default_router)
app.include_router(auth_router)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return app.templates.TemplateResponse("index.html", context={"request": request})
