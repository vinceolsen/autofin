clean:
	echo "cleaning project" && \
	rm -rf .venv && \
	rm -rf venv

install:
	echo "installing dependencies" && \
	pip install --upgrade pip && \
	pip install poetry --extra-index-url=https://pypi.org/simple && \
	poetry config virtualenvs.create true && \
	poetry config virtualenvs.in-project true && \
	poetry install

run:
	poetry run python algofin/src/trading_strategies.py

test:
	echo "running tests"
	poetry run pytest

clean_install: clean install



