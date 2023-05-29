run_service:
	docker-compose up -d

stop_service:
	docker-compose stop

migrate:
	python3 autoru_ripoff/manage.py migrate