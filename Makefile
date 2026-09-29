# Variables
PYTHON = python3
MAIN = main.py
MAP = config.txt

.PHONY: install run debug clean lint lint-strict

# Rule to install dependencies
install:
	pip install flake8 mypy
	@echo "Dependencies installed successfully!"

# Rule to execute the main program
run:
	$(PYTHON) $(MAIN) $(MAP) || true

# Rule to run the program in debug mode using pdb
debug:
	$(PYTHON) -m pdb $(MAIN) $(MAP)

# Rule to clean up cache and temporary files
clean:
	rm -rf __pycache__ .mypy_cache
	find . -type d -name "__pycache__" -exec rm -r {} +
	@echo "Environment cleaned!"

# Rule to run the linter and static type checker
lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

# Optional rule for extra verification
lint-strict:
	flake8 .
	mypy --strict .
