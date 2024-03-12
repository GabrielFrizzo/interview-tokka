#! /usr/bin/env bash
set -e

poetry run celery -A src.background.main worker --loglevel=info -c 2 -B
