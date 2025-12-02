# Email Setup Guide for Data Management System

## Gmail SMTP Configuration

This guide will help you configure the email functionality to send emails from `shyadmusthafa001@gmail.com`.

### Step 1: Enable 2-Factor Authentication

1. Go to your Google Account settings: https://myaccount.google.com/
2. Navigate to "Security"
3. Enable "2-Step Verification" if not already enabled

### Step 2: Generate App Password

1. Go to Google Account settings: https://myaccount.google.com/
2. Navigate to "Security"
3. Under "2-Step Verification", click on "App passwords"
4. Select "Mail" as the app and "Other" as the device
5. Click "Generate"
6. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

### Step 3: Update Django Settings

1. Open `mysite/settings.py`
2. Find the email configuration section
3. Update the `EMAIL_HOST_PASSWORD` with your app password:

```python
# Email Configuration for Gmail SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'shyadmusthafa001@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-character-app-password-here'  # Replace with your app password
DEFAULT_FROM_EMAIL = 'shyadmusthafa001@gmail.com'
SERVER_EMAIL = 'shyadmusthafa001@gmail.com'
```

### Step 4: Test Email Configuration

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. Go to the Mail Reminder page: http://127.0.0.1:8000/mail-reminder/

3. Use the "Email Configuration Test" section to send a test email

4. Check the console output for email delivery status

### Step 5: Production Deployment

For production deployment, you should:

1. Set `DEBUG = False` in settings
2. Use environment variables for sensitive data:

```python
import os

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
```

3. Set the environment variable:
   ```bash
   export EMAIL_HOST_PASSWORD='your-app-password'
   ```

### Troubleshooting

#### Common Issues:

1. **Authentication Error**: Make sure you're using the App Password, not your regular Gmail password
2. **Connection Timeout**: Check your internet connection and firewall settings
3. **SMTP Error**: Verify the email settings are correct

#### Testing in Development:

During development, emails are sent to the console instead of actual SMTP. You'll see them in the terminal output.

#### Security Notes:

- Never commit your app password to version control
- Use environment variables in production
- Regularly rotate your app passwords
- Monitor your Gmail account for any suspicious activity

### Email Templates Available

The system includes the following email templates:

1. **Renewal Reminder**: For SPO Rent agreements due for renewal
2. **Expiry Notice**: For agreements expiring soon
3. **Payment Reminder**: For payment-related communications
4. **General Update**: For general announcements

### Usage

1. Go to Mail Reminder page
2. Click on "SPO Rent Renewal" card
3. Filter and select records
4. Choose email type and add custom message
5. Send emails to selected recipients

### Support

If you encounter any issues:

1. Check the Django console for error messages
2. Verify your Gmail app password is correct
3. Ensure 2-factor authentication is enabled
4. Test with the email configuration test feature

---

**Note**: This setup uses Gmail's SMTP server. For high-volume email sending, consider using dedicated email services like SendGrid, Mailgun, or AWS SES. 