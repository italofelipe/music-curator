from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from core.config import settings

# Engine síncrono (psycopg v3) – ótimo para MVP e simples de testar
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    future=True,
)

# Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)

# Base declarativa
Base = declarative_base()


@contextmanager
def session_scope() -> Iterator[Session]:
    """
    Cria um escopo de sessão transacional.
    @returns {Iterator[Session]} Um gerenciador de contexto com commit/rollback automáticos.
    """
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
