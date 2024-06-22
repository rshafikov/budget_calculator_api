test:
	DB_TEST=True pytest -s

lint:
	isort ./api ./tests
	pylint ./api ./tests
