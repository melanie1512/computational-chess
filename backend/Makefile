.PHONY: test coverage

test:
	pytest ./tests/test.py


coverage:
	pytest --cov=tests

run:
	flask db migrate
	flask db upgrade
	flask run