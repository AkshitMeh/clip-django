#!/bin/bash
cd "$(dirname "$0")"
. .venv/bin/activate
/Users/akshitmehta/Development/Projects/clip-django/.venv/bin/python manage.py delete_expired_pastes
