#!/bin/sh
export FLASK_APP='main'
export FLASK_ENV='development'
export PYTHONDONTWRITEBYTECODE=1
cd ..
python main.py