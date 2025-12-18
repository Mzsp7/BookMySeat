# PythonAnywhere Deployment Guide

Since Render requires a credit card, PythonAnywhere is the best alternative for a free deployment without bank details.

## 1. Create Account
Sign up for a free "Beginner" account at [pythonanywhere.com](https://www.pythonanywhere.com/).

## 2. Open Bash Console
In your PythonAnywhere Dashboard, open a **Bash** console.

## 3. Clone and Setup
Run these commands in order:

```bash
# Clone the repository
git clone https://github.com/Mzsp7/BookMySeat.git
cd BookMySeat

# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 my-env

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Setup Database
python manage.py migrate
python scripts/add_seats.py
```

## 4. Configure Web App
1. Go to the **Web** tab in PythonAnywhere Dashboard.
2. Click **Add a new web app** -> **Next** -> **Manual Configuration** -> **Python 3.10**.
3. **Virtualenv Section**: Set the path to `/home/YOUR_USERNAME/.virtualenvs/my-env`
4. **Code Section**: Edit the **WSGI configuration file** and use this content:

```python
import os
import sys

# Replace YOUR_USERNAME with your actual PythonAnywhere username
path = '/home/YOUR_USERNAME/BookMySeat'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'bookmyseat.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 5. Static Files
In the **Web** tab, scroll to **Static Files**:
- **URL**: `/static/`
- **Path**: `/home/YOUR_USERNAME/BookMySeat/staticfiles`

## 6. Environment Variables
To keep your keys safe on PythonAnywhere:
1. Create a `.env` file in `/home/YOUR_USERNAME/BookMySeat/.env`
2. Add your Stripe/Email keys there (same format as `.env.example`).

## 7. Reload
Click the **Reload** button at the top of the Web tab.

---
**Your site is now live at: `YOUR_USERNAME.pythonanywhere.com`** 🚀
