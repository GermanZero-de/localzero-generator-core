#/bin/sh

set -e

pytest
pre-commit run -a

read -p "You are ready to rock and save the climate at $(git rev-parse HEAD), but don't forget to copy paste the above into your pull request"

