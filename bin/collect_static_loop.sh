#! /bin/sh
while true; do python3.8 manage.py compilestatic --force; sleep 20; done