#!/bin/bash

set -x
MR_PATH="/var/www/html/mr_project"

"$MR_PATH"/manage.py makemigrations
"$MR_PATH"/manage.py migrate

exec "$@"
