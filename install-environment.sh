#!/bin/bash
# Install environment once (poetry and git pre-commit)
set -e

# Poetry
poetry install

# Git pre-commit
poetry run pre-commit install
echo "All done"
