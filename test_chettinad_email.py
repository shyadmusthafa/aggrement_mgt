#!/usr/bin/env python
"""
Test Chettinad Email Configuration
This script tests the new Chettinad email server configuration
"""

import os
import sys
import django
from django.core.mail import send_mail
from django.conf import settings
import smtplib

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def test_chettinad_email_config():
    """Test the Chettinad email configuration"""
    print("=" * 70)
    print("📧 CHETTINAD EMAIL CONFIGURATION TEST")
    print("=" * 70)
    
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

def test_smtp_connection():
    """Test SMTP connection to Chettinad server"""
    print("=" * 70)
    print("🔌 TESTING SMTP CONNECTION TO CHETTINAD SERVER")
    print("=" * 70)
    
    try:
        print(f"Connecting to {settings.EMAIL_HOST}:{settings.EMAIL_PORT}...")
        
        # Create SMTP connection
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        
        print("✅ TLS connection established")
        
        # Try to login
        print(f"Attempting to login with {settings.EMAIL_HOST_USER}...")
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        
        print("✅ SMTP login successful!")
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication Failed: {e}")
        print("Please check your username and password.")
        return False
        
    except Exception as e:
        print(f"❌ SMTP Connection Failed: {e}")
        print("Please check your server settings and network connection.")
        return False

def test_email_sending():
    """Test sending email through Django"""
    print("=" * 70)
    print("📧 TESTING EMAIL SENDING")
    print("=" * 70)
    
    # Test email to the same address
    test_email = settings.EMAIL_HOST_USER
    
    try:
        print(f"Sending test email to {test_email}...")
        
        send_mail(
            subject='Test Email - Data Management System (Chettinad)',
            message=f"""
Hello,

This is a test email from the Data Management System using Chettinad email server.

Email Details:
- From: {settings.DEFAULT_FROM_EMAIL}
- To: {test_email}
- Server: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}
- Sent at: {django.utils.timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

If you receive this email, the Chettinad email configuration is working correctly.

Best regards,
Data Management Team
            """.strip(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        print("✅ Test email sent successfully!")
        print("📬 Check your email inbox (and spam folder) for the test message.")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {str(e)}")
        print()
        print("Common solutions:")
        print("1. Check your username and password")
        print("2. Verify the server settings")
        print("3. Check your network connection")
        print("4. Contact your email administrator if issues persist")
        return False

def main():
    """Main test function"""
    print("🔧 CHETTINAD EMAIL TEST")
    print("Testing the new Chettinad email configuration...")
    print()
    
    # Check configuration
    test_chettinad_email_config()
    
    # Test SMTP connection
    if test_smtp_connection():
        print("✅ SMTP connection successful!")
        print()
        
        # Test email sending
        if test_email_sending():
            print("🎉 EMAIL CONFIGURATION IS WORKING!")
            print("Your Chettinad email setup is complete and functional.")
        else:
            print("❌ Email sending failed. Please check the error above.")
    else:
        print("❌ SMTP connection failed. Please check your credentials and server settings.")

if __name__ == "__main__":
    main() 