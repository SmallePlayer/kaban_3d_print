#!/bin/bash
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python3 src/app.py