#!/usr/bin/env bash
python3 migrate.py db upgrade
python3 -m flask run --host=0.0.0.0
