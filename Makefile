# 🧰 music_curator – DX helpers

## @task setup: Instala deps (local com Poetry) e pre-commit
setup:
	poetry install --with dev
	poetry run pre-commit install

## @task build: Build da imagem da API (sem cache)
build:
	docker compose build --no-cache api

## @task up: Sobe a stack (api, db, admin)
up:
	docker compose up

## @task up-d: Sobe a stack em segundo plano
up-d:
	docker compose up -d

## @task down: Derruba e remove volumes 😬
down:
	docker compose down -v

## @task logs: Segue logs da API
logs:
	docker compose logs -f api

## @task bash: Entra no container da API
bash:
	docker compose run --rm api bash

## @task fmt: Formata com isort+black
fmt:
	poetry run isort .
	poetry run black .

## @task lint: Lint com ruff + mypy
lint:
	poetry run ruff .
	poetry run mypy src

## @task test: Pytest rápido
test:
	poetry run pytest -q

## @task cz: Commit via Conventional Commits (Commitizen)
cz:
	poetry run cz commit

.PHONY: setup build up up-d down logs bash fmt lint test cz
