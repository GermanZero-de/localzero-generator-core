#/bin/sh

set -e

pytest
pre-commit run -a
echo "I'm ready to rock and save the climate"

