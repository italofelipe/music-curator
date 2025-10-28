from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def healthcheck() -> dict:
    """
    Verifica se a API está saudável.
    @returns {{ status: string }} Objeto com status da API.
    """
    return {"status": "ok"}
