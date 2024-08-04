test:
	DB_TEST=True pytest -s

lint: clean
	isort ./api ./tests
	pylint ./api ./tests

db_setup:
	alembic upgrade head

clean:
	find . -name "*.pyc" -delete