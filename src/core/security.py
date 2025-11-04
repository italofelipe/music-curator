from __future__ import annotations

import re
from typing import Final

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Políticas de senha
MIN_LEN: Final[int] = 13
RGX_UPPER: Final[re.Pattern[str]] = re.compile(r"[A-Z]")
RGX_LOWER: Final[re.Pattern[str]] = re.compile(r"[a-z]")
RGX_DIGIT: Final[re.Pattern[str]] = re.compile(r"\d")
RGX_SPECIAL: Final[re.Pattern[str]] = re.compile(r"[^\w\s]")  # símbolo não alfanumérico


def hash_password(plain_password: str) -> str:
    """
    Gera hash seguro para a senha.
    @param {str} plain_password - Senha em texto plano.
    @returns {str} Hash bcrypt.
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    Verifica senha contra o hash.
    @param {str} plain_password - Senha em texto plano.
    @param {str} password_hash - Hash armazenado.
    @returns {bool} True se confere, do contrário False.
    """
    return pwd_context.verify(plain_password, password_hash)


def validate_password_policy(password: str) -> list[str]:
    """
    Valida a senha contra as regras de segurança.
    @param {str} password - Senha para validar.
    @returns {list[str]} Lista de mensagens de erro; vazia se válida.
    """
    errors: list[str] = []
    if len(password) < MIN_LEN:
        errors.append(f"Password must be at least {MIN_LEN} characters long.")
    if not RGX_UPPER.search(password):
        errors.append("Password must contain at least one uppercase letter.")
    if not RGX_LOWER.search(password):
        errors.append("Password must contain at least one lowercase letter.")
    if not RGX_DIGIT.search(password):
        errors.append("Password must contain at least one digit.")
    if not RGX_SPECIAL.search(password):
        errors.append("Password must contain at least one special symbol (e.g., !@#$%).")
    return errors
