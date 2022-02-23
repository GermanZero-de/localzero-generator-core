#/bin/sh

set -e

if ! which -s pyright ; then
  echo "pyright is not installed"
  echo
  echo "Run poetry install to install it."
  exit 1
fi

pyright
pytest
pre-commit run -a

read -p "You are ready to rock and save the climate at $(git rev-parse HEAD), but don't forget to copy paste the above into your pull request"

