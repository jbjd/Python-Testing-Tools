validate:
	ruff check .
	ruff format --check
	mypy . --check-untyped-defs
	codespell .

test: export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
test:
	python -m coverage run --source=personal_testing_tools -m pytest
	@coverage report -m
