#/bin/sh

set -e

if ! which -s pyright ; then
  echo "pyright is not installed"
  echo
  echo "Go and install it. If you have npm installed it's as quick as:"
  echo "  npm install --global pyright"
  echo "or with yarn:"
  echo "  yarn global add pyright"
  echo
  echo "If you have neither go and install one of them first."
  exit 1
fi

pyright
pytest
pre-commit run -a

read -p "You are ready to rock and save the climate at $(git rev-parse HEAD), but don't forget to copy paste the above into your pull request"

