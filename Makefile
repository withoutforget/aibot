init:
	mkdir logs
run:
	docker compose up -d
watch:
	docker compose up --watch
stop:
	docker compose stop
postgres:
	docker compose exec -it 14e2f41ecd36 psql -U admin -d pgdb