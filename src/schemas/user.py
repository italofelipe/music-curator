from __future__ import annotations

from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """
    DTO para criação de usuário.
    @property {EmailStr} email - E-mail válido do usuário.
    @property {str} password - Senha em texto plano (validada pelo service).
    """
    email: EmailStr
    password: str = Field(min_length=13)


class UserOut(BaseModel):
    """
    DTO de retorno ao criar/consultar usuário (sem expor hash).
    @property {UUID} id - UUID do usuário.
    @property {EmailStr} email - E-mail do usuário.
    @property {bool} is_active - Status de ativação.
    """
    id: UUID
    email: EmailStr
    is_active: bool

    model_config = {"from_attributes": True}
