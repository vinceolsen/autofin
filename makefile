clean_results:
	echo "cleaning up old results" && \
	rm -rf algofin/results/*

clean: clean_results
	echo "cleaning project" && \
	rm -rf .pytest_cache && \
	rm -rf .venv && \
	rm -rf venv

install:
	echo "installing dependencies" && \
	pip install --upgrade pip && \
	pip install flake8 && \
	pip install poetry --extra-index-url=https://pypi.org/simple && \
	poetry config virtualenvs.create true && \
	poetry config virtualenvs.in-project true && \
	poetry install

run:
	poetry run python algofin/src/trading_strategies.py

test:
	echo "running tests"
	poetry run pytest

lint:
	echo "running linting"
	poetry run flake8 algofin/src tests

clean_install: clean install

