# Rule to install dependencies
install:
	pip install flake8 mypy
	@echo "Dependencies installed successfully!"

# Rule to execute the main program
run:
	python3 a_maze_ing.py config.txt || true

# Rule to run the program in debug mode using pdb
debug:
	python3 -m pdb a_maze_ing.py config.txt

# Rule to clean up cache and temporary files
clean:
	rm -rf __pycache__ .mypy_cache
	find . -type d -name "__pycache__" -exec rm -r {} +
	@echo "Environment cleaned!"

# Rule to run the linter and static type checker
lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .