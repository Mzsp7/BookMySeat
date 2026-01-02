#!/bin/bash

echo "🎬 BookMyShow Clone - Startup Script"
echo "==================================="

export PYTHONPATH=$PWD

if [ -d ".venv" ]; then
    echo "📦 Activating Virtual Environment..."
    source .venv/bin/activate
else
    echo "⚠️ Virtual environment (.venv) not found. Running globally..."
fi

echo "📦 Checking dependencies..."
pip install -r requirements.txt

echo "🗄️ Applying migrations..."
python3 manage.py migrate

echo "🛋️ Adding default seats if needed..."
python3 scripts/add_seats.py

echo "🚀 Starting server..."
python3 manage.py runserver
