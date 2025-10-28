from fastapi import FastAPI
from src.routers import health

def create_app() -> FastAPI:
    """
    Cria e configura a aplicação FastAPI.
    @returns {FastAPI} Instância configurada da aplicação.
    """
    app = FastAPI(title="music_curator", version="0.1.0")
    app.include_router(health.router, prefix="")
    return app

app = create_app()
