# Gmail Email Setup Guide

## Step 1: Generate Gmail App Password

1. **Go to Google Account Settings**
   - Visit: https://myaccount.google.com/security

2. **Enable 2-Step Verification** (if not already enabled)
   - Click "2-Step Verification"
   - Follow the setup process

3. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Windows Computer" (or Other)
   - Click "Generate"
   - **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

## Step 2: Update settings.py

Open `bookmyseat/settings.py` and update:

```python
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Changed!
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'abcdefghijklmnop'  # Your 16-char app password (no spaces)
```

## Step 3: Restart Server

```bash
# Stop the server (Ctrl+C in terminal)
python manage.py runserver
```

## Step 4: Test

1. Make a booking
2. Check the email inbox of the user who booked
3. You should receive a confirmation email!

## Troubleshooting

### "SMTPAuthenticationError"
- Double-check your email and app password
- Make sure 2-Step Verification is enabled
- Regenerate the app password if needed

### "Connection refused"
- Check your internet connection
- Verify port 587 is not blocked by firewall

### Email not received
- Check spam/junk folder
- Verify the user's email address is correct in their profile
- Check terminal for error messages

## Security Note

**Never commit your real email password to Git!**

Consider using environment variables:

```python
import os
EMAIL_HOST_USER = os.environ.get('EMAIL_USER', 'your-email@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'your-app-password')
```

Then set in your terminal:
```bash
$env:EMAIL_USER = "your-email@gmail.com"
$env:EMAIL_PASSWORD = "your-app-password"
```
