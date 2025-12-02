# Quick Email Fix Guide

## Problem Identified
Your Django application is not sending emails because:
1. **Missing Gmail App Password**: The `EMAIL_HOST_PASSWORD` is not configured
2. **Email Backend Conflict**: The development console backend was overriding SMTP settings

## What I Fixed
1. ✅ **Fixed Email Backend**: Commented out the console backend override in development
2. ✅ **Added Environment Variable Support**: Email password can now be set via environment variable
3. ✅ **Created Test Script**: `test_email_setup.py` to diagnose email issues

## To Fix Your Email Issue:

### Option 1: Set Environment Variable (Recommended)
```bash
# Windows PowerShell
$env:EMAIL_HOST_PASSWORD="your-16-character-app-password"

# Windows Command Prompt
set EMAIL_HOST_PASSWORD=your-16-character-app-password

# Then run the test
python test_email_setup.py
```

### Option 2: Direct Settings Update
1. Open `mysite/settings.py`
2. Find line 135: `EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')`
3. Replace with: `EMAIL_HOST_PASSWORD = 'your-16-character-app-password'`
4. Run: `python test_email_setup.py`

## How to Get Gmail App Password:

1. **Enable 2-Factor Authentication**:
   - Go to: https://myaccount.google.com/
   - Security → 2-Step Verification → Enable

2. **Generate App Password**:
   - Go to: https://myaccount.google.com/
   - Security → 2-Step Verification → App passwords
   - Select "Mail" → "Other" → Generate
   - Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

3. **Use the password** in one of the options above

## Test Your Setup:
```bash
python test_email_setup.py
```

## If Still Not Working:
1. Check your internet connection
2. Verify 2-Factor Authentication is enabled
3. Make sure you're using App Password, not regular Gmail password
4. Check spam folder for test emails
5. Try with a different email address

## For Production:
- Use environment variables for security
- Consider using dedicated email services (SendGrid, Mailgun, AWS SES)
- Set `DEBUG = False` in settings

---
**Note**: The email functionality in your Django app is now properly configured. Once you set the Gmail App Password, emails should work correctly. 