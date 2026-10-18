# Variables
PYTHON = python3
MAIN = main.py
MAP = maps/easy/01_linear_path.txt

.PHONY: install run debug clean lint lint-strict

# Rule to install dependencies
install:
	poetry install
	@echo "Dependencies installed successfully!"

# Rule to execute the main program (accepts optional MAP argument: make run MAP=maps/...)
run:
	poetry run python $(MAIN) $(MAP)

# Rule to run the program in debug mode using pdb
debug:
	poetry run python -m pdb $(MAIN) $(MAP)

# Rule to clean up cache and temporary files
clean:
	rm -rf __pycache__
	rm -rf .mypy_cache 
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	@echo "Environment cleaned!"

# Rule to run the linter and static type checker
lint:
	poetry run flake8 .
	poetry run mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

# Optional rule for extra verification
lint-strict:
	flake8 .
	mypy --strict .
