.PHONY: test run

run:
	@python main.py

test:
	@python -m unittest tests/alerts_test.py
