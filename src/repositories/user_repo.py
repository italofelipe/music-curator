from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models.user import User


class UserRepository:
    """
    Repositório de usuários.
    @function get_by_email - Retorna usuário pelo e-mail.
    @function create - Persiste novo usuário.
    """

    def __init__(self, session: Session) -> None:
        """
        Injeta a sessão do banco.
        @param {Session} session - Sessão SQLAlchemy.
        """
        self._session = session

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Busca usuário por e-mail.
        @param {str} email - E-mail normalizado.
        @returns {Optional[User]} Usuário encontrado ou None.
        """
        stmt = select(User).where(User.email == email.lower())
        return self._session.execute(stmt).scalars().first()

    def create(self, email: str, password_hash: str) -> User:
        """
        Cria e persiste usuário.
        @param {str} email - E-mail normalizado.
        @param {str} password_hash - Hash bcrypt da senha.
        @returns {User} Usuário persistido.
        """
        user = User(email=email.lower(), password_hash=password_hash)
        self._session.add(user)
        self._session.flush()  # obtém PK imediatamente
        return user
