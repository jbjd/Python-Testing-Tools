validate:
	ruff check .
	ruff format --check
	mypy . --check-untyped-defs
	codespell personal_testing_tools setup.py tests .ruff.toml README.md

override PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
export PYTEST_DISABLE_PLUGIN_AUTOLOAD

test:
	python -m coverage run --source=personal_testing_tools -m pytest
	@coverage report -m
