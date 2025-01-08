#!/bin/sh
cd /app
exec .venv/bin/watchmedo auto-restart -d=. -p=*.py -R /.venv/bin/python run.py