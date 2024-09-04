up-db:
	docker compose -f ./dev/db/docker-compose.yml up -d

down-db:
	docker compose -f ./dev/db/docker-compose.yml down

# example: make makemigrations revision=init_user_model
makemigrations:
	poetry run alembic revision --autogenerate -m "${revision}"

migrate:
	poetry run alembic upgrade head

run:
	poetry run python -m main
