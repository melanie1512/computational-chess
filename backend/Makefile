.PHONY: test coverage

test:
	pytest ./tests/test.py


coverage:
	pytest --cov=tests

run:
	flask db upgrade
	flask db migrate
	flask run