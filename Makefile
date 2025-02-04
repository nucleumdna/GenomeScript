.PHONY: install test lint format check docker-build docker-run dev test-local clean

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

lint:
	pylint src/ tests/
	mypy src/ tests/

format:
	black src/ tests/
	isort src/ tests/

check: format lint test

docker-build:
	docker-compose build

docker-run:
	docker-compose up

dev:
	./scripts/dev.sh

test-local:
	pytest tests/test_local.py -v

clean:
	rm -rf venv
	rm -rf frontend/node_modules
	rm -rf test_data
	rm -f dev.db 