init:
	mkdir logs
run:
	docker compose up --verbose
watch:
	docker compose up --watch
stop:
	docker compose stop
build:
	docker compose build
postgres:
	docker compose exec -it 14e2f41ecd36 psql -U admin -d pgdb
migrate:
	uv run alembic upgrade head
makemigrate:
	uv run alembic revision --autogenerate -m "initial"