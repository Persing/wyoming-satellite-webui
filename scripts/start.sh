#!/bin/bash

# Start the Wyoming Satellite Web Portal

cd /opt/wyoming-satellite-web
source .venv/bin/activate
python3 backend/app.py