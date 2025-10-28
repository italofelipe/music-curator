# music_curator

MVP: Login (email/senha), conectar ao Spotify, ler músicas curtidas e gerar playlists com GPT.

## Stack

- Docker, Docker Compose
- FastAPI (Python 3.14)
- PostgreSQL 16 + pgAdmin
- Poetry, Ruff, Black, isort, mypy, Pytest
- Commitizen (Conventional Commits)

## Rodando

```bash
cp .env.example .env   # preencha chaves
docker compose build --no-cache api
docker compose up
# API: http://localhost:8000/docs
# Health: http://localhost:8000/health
# pgAdmin: http://localhost:5050
```

## Dev Utils

make setup # poetry + pre-commit
make fmt # format
make lint # lint
make test # tests

## Estrutura

src/
music_curator/
**init**.py
main.py
routers/
health.py
alembic/
versions/
alembic.ini
Dockerfile
docker-compose.yml
pyproject.toml
