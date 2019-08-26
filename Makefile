.PHONY: shell test run

shell:
	@pipenv shell

run:
	@python main.py

test:
	@python -m unittest tests/koel_tests.py
