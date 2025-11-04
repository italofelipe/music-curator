from __future__ import annotations

from fastapi import FastAPI

from routers.health import router as health_router
from routers.users import router as users_router


def create_app() -> FastAPI:
    """
    Factory da aplicação FastAPI.
    @returns {FastAPI} Instância configurada.
    """
    app = FastAPI(title="music_curator", version="0.1.0")
    app.include_router(health_router)
    app.include_router(users_router)
    return app


app = create_app()
