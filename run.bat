@echo off
setlocal

echo Starting BookMyShow Clone...
set PYTHONPATH=%CD%

if not exist .venv\Scripts\activate.bat goto no_venv
echo Activating Virtual Environment...
call .venv\Scripts\activate.bat
goto start_app

:no_venv
echo Virtual environment not found. Running globally...

:start_app
echo Checking dependencies...
pip install -r requirements.txt

echo Applying migrations...
python manage.py migrate

echo Adding default seats...
python scripts/add_seats.py

echo Starting server...
python manage.py runserver
