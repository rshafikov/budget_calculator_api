clean:
	find . -name "*.pyc" -delete
	find . -name "*.log" -delete

dist: clean lint
	python3 setup.py sdist

lint: sort
	pycodestyle --exclude=venv,migrations,settings.py .

sort:
	isort .

run_app: clean lint
	docker compose -f ./compose/docker-compose.yaml down
	docker compose -f ./compose/docker-compose.yaml up -d
