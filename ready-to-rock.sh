#/bin/sh

set -e

pytest
pre-commit run -a
echo "I'm ready to rock and save the climate"

read -p "You are ready to rock and save the climate, but don't forget to copy paste the above into your pull request"

