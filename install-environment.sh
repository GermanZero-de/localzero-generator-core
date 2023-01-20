#!/bin/bash
# Install environment once (poetry and git pre-commit)
set -e

# Poetry
poetry install --dev --no-root

# Git pre-commit
poetry run pre-commit install

echo "All done"
