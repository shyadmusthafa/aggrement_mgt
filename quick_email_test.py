#!/usr/bin/env python
"""
Quick Email Test Script
Tests the current email configuration and provides immediate feedback
"""

import os
import sys
import django
from django.core.mail import send_mail
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def test_email():
    """Quick email test"""
    print("=" * 50)
    print("QUICK EMAIL TEST")
    print("=" * 50)
    
    print(f"Email User: {settings.EMAIL_HOST_USER}")
    print(f"Email Password: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    print()
    
    # Test email to the same address
    test_email = settings.EMAIL_HOST_USER
    
    try:
        print(f"📧 Sending test email to {test_email}...")
        
        send_mail(
            subject='Test Email - Data Management System',
            message='This is a test email to verify email configuration.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        print("✅ Email sent successfully!")
        print("Check your inbox (and spam folder) for the test email.")
        
    except Exception as e:
        print(f"❌ Email failed: {str(e)}")
        print()
        print("🔧 SOLUTION:")
        print("You need to use a Gmail App Password, not your regular password.")
        print()
        print("Follow these steps:")
        print("1. Go to: https://myaccount.google.com/")
        print("2. Security → 2-Step Verification → Enable")
        print("3. Security → 2-Step Verification → App passwords")
        print("4. Select 'Mail' → 'Other' → Generate")
        print("5. Copy the 16-character password")
        print("6. Update settings.py with the App Password")
        print()
        print("Current error suggests authentication failed with regular password.")

if __name__ == "__main__":
    test_email() 