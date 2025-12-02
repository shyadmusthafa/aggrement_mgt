#!/usr/bin/env python
"""
Email Troubleshooter - Comprehensive Email Fix Script
This script will help you diagnose and fix email issues step by step
"""

import os
import sys
import django
from django.core.mail import send_mail
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def check_current_settings():
    """Check current email settings"""
    print("=" * 70)
    print("📧 EMAIL SETTINGS DIAGNOSIS")
    print("=" * 70)
    
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
    """Test SMTP connection directly"""
    print("=" * 70)
    print("🔌 TESTING SMTP CONNECTION")
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
        print()
        print("🔧 SOLUTION: You need a Gmail App Password")
        print("The error indicates you're using a regular password instead of an App Password.")
        return False
        
    except Exception as e:
        print(f"❌ SMTP Connection Failed: {e}")
        return False

def test_django_email():
    """Test Django email sending"""
    print("=" * 70)
    print("📧 TESTING DJANGO EMAIL")
    print("=" * 70)
    
    test_email = settings.EMAIL_HOST_USER
    
    try:
        print(f"Sending test email to {test_email}...")
        
        send_mail(
            subject='Email Test - Data Management System',
            message='This is a test email to verify your email configuration is working.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        print("✅ Django email sent successfully!")
        print("📬 Check your email inbox (and spam folder) for the test message.")
        return True
        
    except Exception as e:
        print(f"❌ Django email failed: {e}")
        return False

def interactive_app_password_setup():
    """Interactive App Password setup"""
    print("=" * 70)
    print("🔑 GMAIL APP PASSWORD SETUP")
    print("=" * 70)
    
    print("To fix your email issue, you need to get a Gmail App Password.")
    print()
    
    # Check if user has App Password
    choice = input("Do you have your Gmail App Password? (yes/no): ").strip().lower()
    
    if choice in ['yes', 'y']:
        app_password = input("Enter your 16-character App Password: ").strip()
        
        if len(app_password) == 16:
            print()
            print("Updating settings with your App Password...")
            
            # Update the settings file
            settings_file = 'mysite/settings.py'
            try:
                with open(settings_file, 'r') as f:
                    content = f.read()
                
                # Find and replace the password line
                old_pattern = "EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '"
                new_pattern = f"EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '{app_password}')"
                
                if old_pattern in content:
                    # Find the line and replace it
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if line.strip().startswith('EMAIL_HOST_PASSWORD = os.environ.get'):
                            lines[i] = new_pattern
                            break
                    
                    content = '\n'.join(lines)
                    
                    with open(settings_file, 'w') as f:
                        f.write(content)
                    
                    print("✅ Settings updated successfully!")
                    print("Testing email configuration...")
                    print()
                    
                    # Reload Django settings
                    django.setup()
                    
                    # Test the new configuration
                    if test_smtp_connection() and test_django_email():
                        print("🎉 EMAIL IS NOW WORKING!")
                        print("You should receive the test email shortly.")
                    else:
                        print("❌ Still having issues. Please check your App Password.")
                        
                else:
                    print("❌ Could not find the EMAIL_HOST_PASSWORD line in settings.py")
                    
            except Exception as e:
                print(f"❌ Error updating settings: {str(e)}")
        else:
            print("❌ App Password should be exactly 16 characters long.")
    else:
        show_app_password_instructions()

def show_app_password_instructions():
    """Show detailed App Password instructions"""
    print("=" * 70)
    print("📋 HOW TO GET GMAIL APP PASSWORD")
    print("=" * 70)
    print()
    print("STEP 1: Enable 2-Factor Authentication")
    print("1. Go to: https://myaccount.google.com/")
    print("2. Click 'Security' in the left sidebar")
    print("3. Find '2-Step Verification' and click 'Get started'")
    print("4. Follow the setup process to enable 2-Factor Authentication")
    print()
    print("STEP 2: Generate App Password")
    print("1. Go to: https://myaccount.google.com/")
    print("2. Click 'Security' in the left sidebar")
    print("3. Under '2-Step Verification', click 'App passwords'")
    print("4. Select 'Mail' from the dropdown")
    print("5. Select 'Other (Custom name)' from device dropdown")
    print("6. Enter name: 'Data Management System'")
    print("7. Click 'Generate'")
    print("8. COPY the 16-character password (e.g., 'abcd efgh ijkl mnop')")
    print()
    print("STEP 3: Test Again")
    print("Run this script again: python email_troubleshooter.py")
    print()

def check_common_issues():
    """Check for common email issues"""
    print("=" * 70)
    print("🔍 COMMON ISSUES CHECK")
    print("=" * 70)
    
    issues_found = []
    
    # Check if password is set
    if not settings.EMAIL_HOST_PASSWORD:
        issues_found.append("❌ EMAIL_HOST_PASSWORD is not set")
    
    # Check if using regular password (common mistake)
    if settings.EMAIL_HOST_PASSWORD and len(settings.EMAIL_HOST_PASSWORD) < 16:
        issues_found.append("❌ Password appears to be too short (should be 16 characters)")
    
    # Check if email user is set
    if not settings.EMAIL_HOST_USER:
        issues_found.append("❌ EMAIL_HOST_USER is not set")
    
    if issues_found:
        print("Issues found:")
        for issue in issues_found:
            print(f"  {issue}")
        print()
        print("🔧 RECOMMENDED SOLUTION:")
        print("Get a Gmail App Password and update your settings.")
    else:
        print("✅ No obvious configuration issues found.")
        print("The problem might be with the App Password itself.")

def main():
    """Main troubleshooting function"""
    print("🔧 EMAIL TROUBLESHOOTER")
    print("This script will help you fix your email configuration.")
    print()
    
    # Check current settings
    check_current_settings()
    
    # Check for common issues
    check_common_issues()
    
    print()
    
    # Test SMTP connection
    if test_smtp_connection():
        # If SMTP works, test Django email
        test_django_email()
    else:
        # If SMTP fails, offer App Password setup
        print()
        interactive_app_password_setup()

if __name__ == "__main__":
    main() 