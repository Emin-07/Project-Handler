.PHONY: run setup test demo

setup:
	docker-compose up -d db
	sleep 5
	python -m alembic upgrade head

run:
	docker-compose up --build

test:
	pytest -v

demo:
	@echo "Starting demo environment..."
	docker-compose -f docker-compose.demo.yml up --build

down:
	docker-compose down