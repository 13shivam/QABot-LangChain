.PHONY: install-web install-worker run-web run-worker run-all

install-web:
	pip install -r requirements.txt

install-worker:
	pip install -r requirements.txt

install-kafka:
	docker-compose -f docker-compose-kafka.yml up -d

remove-kafka:
	docker-compose -f docker-compose-kafka.yml down -d

run-web:
	uvicorn app.main:web_app --host 0.0.0.0 --port 8000 --reload --log-level info

run-worker:
	uvicorn app.worker_main:worker_app --host 0.0.0.0 --port 8001 --reload --log-level info

run-all:
	@echo "Starting web application in the background..."
	@make run-web &

	@echo "Starting worker application in the background..."
	@make run-worker &
