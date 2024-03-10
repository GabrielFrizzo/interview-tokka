#! /usr/bin/env bash
set -e

celery -A src.background.main worker -c 1
