# Environment Setup Guide

## Setting Up Environment Variables

For security, sensitive credentials are stored in environment variables instead of being hardcoded.

### For Local Development (Windows PowerShell)

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Then edit `.env` with your actual values:

```env
STRIPE_PUBLIC_KEY=pk_test_your_actual_key
STRIPE_SECRET_KEY=sk_test_your_actual_key
STRIPE_WEBHOOK_SECRET=whsec_your_actual_secret
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Loading Environment Variables

#### Option 1: Using python-dotenv (Recommended)

1. Install python-dotenv:
```bash
pip install python-dotenv
```

2. Add to `manage.py` (already done):
```python
from dotenv import load_dotenv
load_dotenv()
```

#### Option 2: Set in PowerShell Session

```powershell
$env:STRIPE_PUBLIC_KEY = "pk_test_your_key"
$env:STRIPE_SECRET_KEY = "sk_test_your_key"
$env:STRIPE_WEBHOOK_SECRET = "whsec_your_secret"
$env:EMAIL_HOST_USER = "your-email@gmail.com"
$env:EMAIL_HOST_PASSWORD = "your-app-password"
```

### For Production Deployment

Set environment variables in your hosting platform:

**Heroku:**
```bash
heroku config:set STRIPE_PUBLIC_KEY=pk_live_xxx
heroku config:set STRIPE_SECRET_KEY=sk_live_xxx
```

**Render/Railway:**
- Go to Environment Variables section in dashboard
- Add each variable

**AWS/Azure:**
- Use their respective secrets management services

### Getting Your Credentials

#### Stripe Keys
1. Go to https://dashboard.stripe.com/test/apikeys
2. Copy your Publishable key (starts with `pk_test_`)
3. Copy your Secret key (starts with `sk_test_`)
4. For webhook secret, run: `stripe listen --forward-to localhost:8000/movies/webhook/stripe/`

#### Gmail App Password
1. Go to https://myaccount.google.com/apppasswords
2. Generate an app password for "Mail"
3. Copy the 16-character password

### Security Notes

⚠️ **NEVER commit `.env` file to Git!**
✅ `.env` is already in `.gitignore`
✅ Use `.env.example` as a template (safe to commit)
✅ Rotate keys if accidentally exposed
✅ Use different keys for development and production

### Verifying Setup

Run this to check if environment variables are loaded:

```bash
python -c "import os; print('Stripe Key:', os.environ.get('STRIPE_PUBLIC_KEY', 'NOT SET'))"
```

If you see "NOT SET", the environment variables aren't loaded correctly.
