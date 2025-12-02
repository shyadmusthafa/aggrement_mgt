#!/usr/bin/env python
"""
Email Fix Script - Comprehensive Solution
This script will help you fix the email issue step by step
"""

import os
import sys
import django
from django.core.mail import send_mail
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def check_current_config():
    """Check current email configuration"""
    print("=" * 60)
    print("CURRENT EMAIL CONFIGURATION")
    print("=" * 60)
    print(f"Email User: {settings.EMAIL_HOST_USER}")
    print(f"Email Password: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    print(f"Email Host: {settings.EMAIL_HOST}")
    print(f"Email Port: {settings.EMAIL_PORT}")
    print(f"Email Use TLS: {settings.EMAIL_USE_TLS}")
    print()

def test_email_connection():
    """Test email connection"""
    print("=" * 60)
    print("TESTING EMAIL CONNECTION")
    print("=" * 60)
    
    try:
        print(f"📧 Attempting to send test email to {settings.EMAIL_HOST_USER}...")
        
        send_mail(
            subject='Email Test - Data Management System',
            message='This is a test email to verify your email configuration is working.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        
        print("✅ SUCCESS! Email sent successfully!")
        print("📬 Check your email inbox (and spam folder) for the test message.")
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ FAILED! Email error: {error_msg}")
        print()
        
        if "Username and Password not accepted" in error_msg:
            print("🔧 DIAGNOSIS: Gmail App Password Required")
            print()
            print("The error indicates you're using a regular Gmail password instead of an App Password.")
            print("Gmail requires App Passwords for SMTP authentication.")
            print()
            show_app_password_instructions()
        elif "Authentication failed" in error_msg:
            print("🔧 DIAGNOSIS: Authentication Failed")
            print("This could be due to:")
            print("1. Wrong password")
            print("2. 2-Factor Authentication not enabled")
            print("3. Using regular password instead of App Password")
            print()
            show_app_password_instructions()
        else:
            print("🔧 DIAGNOSIS: Unknown Error")
            print("Please check your internet connection and try again.")
        
        return False

def show_app_password_instructions():
    """Show detailed App Password instructions"""
    print("=" * 60)
    print("HOW TO FIX: GET GMAIL APP PASSWORD")
    print("=" * 60)
    print()
    print("STEP 1: Enable 2-Factor Authentication")
    print("1. Go to: https://myaccount.google.com/")
    print("2. Click 'Security' in the left sidebar")
    print("3. Find '2-Step Verification' and click 'Get started'")
    print("4. Follow the setup process")
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
    print("STEP 3: Update Settings")
    print("1. Open 'mysite/settings.py'")
    print("2. Find this line:")
    print("   EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'Shyad@2025')")
    print("3. Replace 'Shyad@2025' with your new App Password:")
    print("   EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your-16-char-app-password')")
    print()
    print("STEP 4: Test Again")
    print("Run this script again: python fix_email_now.py")
    print()

def interactive_fix():
    """Interactive fix option"""
    print("=" * 60)
    print("QUICK FIX OPTION")
    print("=" * 60)
    print()
    print("If you have your Gmail App Password ready, I can help you update the settings.")
    print()
    
    choice = input("Do you have your Gmail App Password? (yes/no): ").strip().lower()
    
    if choice in ['yes', 'y']:
        app_password = input("Enter your 16-character App Password: ").strip()
        
        if len(app_password) == 16:
            print()
            print("Updating settings...")
            
            # Update the settings file
            settings_file = 'mysite/settings.py'
            try:
                with open(settings_file, 'r') as f:
                    content = f.read()
                
                # Replace the password
                old_line = "EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'Shyad@2025')"
                new_line = f"EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '{app_password}')"
                
                if old_line in content:
                    content = content.replace(old_line, new_line)
                    
                    with open(settings_file, 'w') as f:
                        f.write(content)
                    
                    print("✅ Settings updated successfully!")
                    print("Testing email configuration...")
                    print()
                    
                    # Reload Django settings
                    django.setup()
                    
                    # Test again
                    if test_email_connection():
                        print("🎉 EMAIL IS NOW WORKING!")
                    else:
                        print("❌ Still having issues. Please check the App Password.")
                else:
                    print("❌ Could not find the password line in settings.py")
                    
            except Exception as e:
                print(f"❌ Error updating settings: {str(e)}")
        else:
            print("❌ App Password should be exactly 16 characters long.")
    else:
        print("Please get your Gmail App Password first, then run this script again.")

def main():
    """Main function"""
    print("🔧 EMAIL FIX SCRIPT")
    print("This script will help you fix your email configuration.")
    print()
    
    check_current_config()
    
    # Test current configuration
    if test_email_connection():
        print("🎉 Your email is working correctly!")
    else:
        print()
        interactive_fix()

if __name__ == "__main__":
    main() 