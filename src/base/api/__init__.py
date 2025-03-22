from .main import app as http_app
from .router import admin_router, secure_router

http_app.include_router(admin_router)
http_app.include_router(secure_router)
