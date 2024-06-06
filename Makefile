test:
	pytest -s

lint:
	isort ./api ./tests
	pylint ./api ./tests
