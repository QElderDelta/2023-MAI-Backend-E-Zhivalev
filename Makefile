run_service:
	docker-compose up -d

run_service_build:
	docker-compose up --build -d

stop_service:
	docker-compose stop

migrate:
	python3 autoru_ripoff/manage.py migrate