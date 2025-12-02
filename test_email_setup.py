#!/usr/bin/env python
"""
Email Configuration Test Script
This script helps test and diagnose email configuration issues.
"""

import os
import sys
import django
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ImproperlyConfigured

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def test_email_configuration():
    """Test the current email configuration"""
    print("=" * 60)
    print("EMAIL CONFIGURATION TEST")
    print("=" * 60)
    
    # Check current email settings
    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    print(f"Email Host: {settings.EMAIL_HOST}")
    print(f"Email Port: {settings.EMAIL_PORT}")
    print(f"Email Use TLS: {settings.EMAIL_USE_TLS}")
    print(f"Email Host User: {settings.EMAIL_HOST_USER}")
    print(f"Email Host Password: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
    print(f"Default From Email: {settings.DEFAULT_FROM_EMAIL}")
    print(f"Server Email: {settings.SERVER_EMAIL}")
    print()
    
    # Check if password is set
    if not settings.EMAIL_HOST_PASSWORD:
        print("❌ ERROR: EMAIL_HOST_PASSWORD is not set!")
        print()
        print("To fix this:")
        print("1. Go to your Google Account settings: https://myaccount.google.com/")
        print("2. Navigate to Security > 2-Step Verification")
        print("3. Click on 'App passwords'")
        print("4. Generate a new app password for 'Mail'")
        print("5. Copy the 16-character password")
        print("6. Update mysite/settings.py with:")
        print("   EMAIL_HOST_PASSWORD = 'your-16-character-app-password'")
        print()
        return False
    
    # Test email sending
    test_email = input("Enter a test email address to send a test email: ").strip()
    
    if not test_email:
        print("❌ No email address provided. Exiting.")
        return False
    
    try:
        print(f"\n📧 Sending test email to {test_email}...")
        
        subject = 'Test Email from Data Management System'
        message = f"""
Hello,

This is a test email from the Data Management System to verify email configuration.

Email Details:
- From: {settings.DEFAULT_FROM_EMAIL}
- To: {test_email}
- Backend: {settings.EMAIL_BACKEND}
- Host: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}

If you receive this email, the email configuration is working correctly.

Best regards,
Data Management Team
        """.strip()
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        print("✅ Test email sent successfully!")
        print("Check your email inbox (and spam folder) for the test message.")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {str(e)}")
        print()
        print("Common solutions:")
        print("1. Make sure you're using a Gmail App Password, not your regular password")
        print("2. Ensure 2-Factor Authentication is enabled on your Gmail account")
        print("3. Check your internet connection")
        print("4. Verify the email settings in mysite/settings.py")
        return False

def check_gmail_setup():
    """Provide instructions for Gmail setup"""
    print("=" * 60)
    print("GMAIL SETUP INSTRUCTIONS")
    print("=" * 60)
    print()
    print("To enable email sending with Gmail, follow these steps:")
    print()
    print("1. Enable 2-Factor Authentication:")
    print("   - Go to: https://myaccount.google.com/")
    print("   - Navigate to Security > 2-Step Verification")
    print("   - Enable it if not already enabled")
    print()
    print("2. Generate App Password:")
    print("   - Go to: https://myaccount.google.com/")
    print("   - Navigate to Security > 2-Step Verification")
    print("   - Click on 'App passwords'")
    print("   - Select 'Mail' as the app and 'Other' as the device")
    print("   - Click 'Generate'")
    print("   - Copy the 16-character password (e.g., 'abcd efgh ijkl mnop')")
    print()
    print("3. Update Django Settings:")
    print("   - Open mysite/settings.py")
    print("   - Find the EMAIL_HOST_PASSWORD line")
    print("   - Replace the empty string with your app password:")
    print("     EMAIL_HOST_PASSWORD = 'your-16-character-app-password'")
    print()
    print("4. Test the configuration:")
    print("   - Run this script again: python test_email_setup.py")
    print()

if __name__ == "__main__":
    try:
        # Check if password is set first
        if not settings.EMAIL_HOST_PASSWORD:
            print("❌ EMAIL_HOST_PASSWORD is not configured!")
            print()
            check_gmail_setup()
        else:
            test_email_configuration()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Make sure you're running this script from the project root directory.") 