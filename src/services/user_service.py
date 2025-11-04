from __future__ import annotations

from typing import Tuple

from sqlalchemy.orm import Session

from repositories.user_repo import UserRepository
from core.security import hash_password, validate_password_policy


class UserService:
    """
    Regras de negócio de usuários.
    @function create_user - Valida senha e-mail, verifica unicidade e cria usuário.
    """

    def __init__(self, session: Session) -> None:
        """
        Injeta a sessão.
        @param {Session} session - Sessão SQLAlchemy.
        """
        self._repo = UserRepository(session)

    def create_user(self, email: str, raw_password: str) -> Tuple[bool, str | None, object | None]:
        """
        Cria usuário com validação de política de senha e unicidade de e-mail.
        @param {str} email - E-mail do usuário.
        @param {str} raw_password - Senha em texto plano.
        @returns {(bool, str|None, object|None)} Tupla (ok, error_msg, user_or_none).
        """
        # valida senha
        pwd_errors = validate_password_policy(raw_password)
        if pwd_errors:
            return False, "; ".join(pwd_errors), None

        # verifica e-mail duplicado
        existing = self._repo.get_by_email(email)
        if existing:
            return False, "Email already registered.", None

        # cria
        ph = hash_password(raw_password)
        user = self._repo.create(email=email, password_hash=ph)
        return True, None, user
