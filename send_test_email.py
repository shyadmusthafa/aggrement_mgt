#!/usr/bin/env python
"""
Simple script to send a test email to any specified address
"""
import os
import django
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail

def send_test_email_to(recipient_email):
    """Send a test email to the specified recipient"""
    print("=" * 60)
    print("📧 SENDING TEST EMAIL")
    print("=" * 60)
    
    try:
        print(f"From: {settings.DEFAULT_FROM_EMAIL}")
        print(f"To: {recipient_email}")
        print(f"Server: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        print()
        
        send_mail(
            subject='Test Email - Data Management System',
            message=f"""
Hello,

This is a test email from the Data Management System.

Email Details:
- From: {settings.DEFAULT_FROM_EMAIL}
- To: {recipient_email}
- Server: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}
- Sent at: {django.utils.timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

If you receive this email, the email configuration is working correctly.

Best regards,
Data Management Team
            """.strip(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        
        print("✅ Test email sent successfully!")
        print(f"📬 Check the inbox for: {recipient_email}")
        print("📁 Also check the spam/junk folder")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {str(e)}")
        return False

if __name__ == "__main__":
    # You can change this email address to any address you want to test
    test_recipient = "chettinadsdc@chettinad.com"  # Default recipient
    
    print("🔧 EMAIL TEST SCRIPT")
    print("This script will send a test email to verify the email configuration.")
    print()
    
    # Ask user for recipient email
    user_input = input(f"Enter recipient email address (or press Enter for default '{test_recipient}'): ").strip()
    
    if user_input:
        test_recipient = user_input
    
    print(f"\nSending test email to: {test_recipient}")
    print()
    
    send_test_email_to(test_recipient) 