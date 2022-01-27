#!/bin/bash
# Install environmnet once (poetry and git pre-commit)
set -e

# Poetry
pip install cleo tomlkit poetry.core requests cachecontrol cachy html5lib pkginfo virtualenv lockfile
pip install pexpect
pip install shellingham
poetry install

# Git pre-commit
pre-commit install
echo "All done"