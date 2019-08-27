.PHONY: shell test run format sort_imports lint

shell:
	@pipenv shell

run:
	@python main.py

test:
	@python -m unittest tests/koel_tests.py

format:
	@pipenv run black **/*.py

sort_imports:
	@pipenv run isort **/*.py

lint:
	@pipenv run flake8
