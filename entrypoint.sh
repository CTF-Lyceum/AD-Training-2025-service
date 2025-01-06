#!/bin/sh

echo "service:$USER_PASSWORD" | chpasswd
/usr/sbin/sshd

exec /.venv/bin/watchmedo auto-restart -d=. -p=*.py -R /.venv/bin/python run.py