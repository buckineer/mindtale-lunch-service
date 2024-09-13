#!/bin/sh

# Run mypy for type checking across all Python files in the current directory.
mypy .

# Use autopep8 to automatically format all Python files in the current directory (and subdirectories)
# to comply with PEP 8 standards. This includes removing unused imports and variables.
autopep8 --in-place --recursive .

# Execute flake8 to perform a PEP 8 style guide enforcement check on all Python files in the current directory.
# This helps identify styling issues not automatically fixed by autopep8.
flake8 .

# Use isort to sort and organize imports in all Python files in the current directory (and subdirectories).
# This helps in maintaining a consistent order of imports, making the code more readable and organized.
isort .