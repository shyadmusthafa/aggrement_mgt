# Gmail App Password Setup Guide

## ❌ Current Problem
Your email is failing because Gmail requires an **App Password** for SMTP authentication, not your regular password.

**Error**: `(535, b'5.7.8 Username and Password not accepted')`

## ✅ Solution: Get Gmail App Password

### Step 1: Enable 2-Factor Authentication
1. Go to: https://myaccount.google.com/
2. Click on **Security** in the left sidebar
3. Find **2-Step Verification** and click **Get started**
4. Follow the setup process to enable 2-Factor Authentication

### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/
2. Click on **Security** in the left sidebar
3. Under **2-Step Verification**, click on **App passwords**
4. You may need to sign in again
5. Select **Mail** from the dropdown
6. Select **Other (Custom name)** from the device dropdown
7. Enter a name like "Data Management System"
8. Click **Generate**
9. **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

### Step 3: Update Django Settings
1. Open `mysite/settings.py`
2. Find this line:
   ```python
   EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'Shyad@2025')
   ```
3. Replace `'Shyad@2025'` with your new App Password:
   ```python
   EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your-16-character-app-password')
   ```

### Step 4: Test the Configuration
```bash
python quick_email_test.py
```

## 🔒 Security Notes
- **Never** use your regular Gmail password for SMTP
- **Always** use App Passwords for applications
- App Passwords are 16 characters long
- You can revoke App Passwords anytime from Google Account settings

## 🚨 Important
- The password `Shyad@2025` you provided is your regular Gmail password
- Gmail blocks SMTP access with regular passwords for security
- Only App Passwords work with SMTP

## 📧 After Setup
Once you have the App Password:
1. Update `mysite/settings.py`
2. Run `python quick_email_test.py`
3. Check your email inbox for the test message
4. Your Django application emails will work correctly

## 🆘 If Still Having Issues
1. Make sure 2-Factor Authentication is enabled
2. Verify you copied the App Password correctly (16 characters)
3. Check your spam folder for test emails
4. Try generating a new App Password if needed

---
**Note**: This is a one-time setup. Once configured, your email functionality will work permanently. 