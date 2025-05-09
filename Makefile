init:
	mkdir logs
run:
	docker compose up --verbose
watch:
	docker compose up --watch
stop:
	docker compose stop
postgres:
	docker compose exec -it 14e2f41ecd36 psql -U admin -d pgdb
migrate:
	docker compose run --rm alembic uv run alembic upgrade head