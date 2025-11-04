from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import SessionLocal
from schemas.user import UserCreate, UserOut
from services.user_service import UserService

router = APIRouter(prefix="/register", tags=["register"])


def get_db() -> Session:
    """
    Fornece uma sessão do banco por request.
    @returns {Session} Sessão SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    """
    Cria um novo usuário.
    @param {UserCreate} payload - Dados de criação (email, password).
    @returns {UserOut} DTO do usuário criado (sem hash).
    """
    service = UserService(db)
    ok, error, user = service.create_user(email=payload.email, raw_password=payload.password)
    if not ok or user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error or "Invalid data")

    return UserOut.model_validate(user)
