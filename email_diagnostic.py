#!/usr/bin/env python
"""
Email Diagnostic Script - Comprehensive Email Issue Diagnosis
This script will help identify the specific cause of "mail not send" issues
"""

import os
import sys
import django
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def check_django_server():
    """Check if Django server is running"""
    print("=" * 60)
    print("🔍 CHECKING DJANGO SERVER")
    print("=" * 60)
    
    try:
        # Try to connect to the Django server
        response = requests.get('http://127.0.0.1:8000/', timeout=5)
        if response.status_code == 200:
            print("✅ Django server is running on http://127.0.0.1:8000/")
            return True
        else:
            print(f"⚠️ Django server responded with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Django server is not running on http://127.0.0.1:8000/")
        print("   Start the server with: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Error checking Django server: {str(e)}")
        return False

def test_email_endpoints():
    """Test the email-related endpoints"""
    print("=" * 60)
    print("🔍 TESTING EMAIL ENDPOINTS")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    endpoints = [
        "/dashboard/mail-reminder/",
        "/dashboard/mail-reminder/spo-rent/",
        "/dashboard/mail-reminder/test-email/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint} - OK (Status: {response.status_code})")
            elif response.status_code == 302:
                print(f"⚠️ {endpoint} - Redirect (Status: {response.status_code}) - Login required")
            else:
                print(f"❌ {endpoint} - Error (Status: {response.status_code})")
        except Exception as e:
            print(f"❌ {endpoint} - Connection failed: {str(e)}")

def check_email_settings():
    """Check email settings in detail"""
    print("=" * 60)
    print("📧 EMAIL SETTINGS DETAILED CHECK")
    print("=" * 60)
    
    settings_to_check = [
        'EMAIL_BACKEND',
        'EMAIL_HOST',
        'EMAIL_PORT',
        'EMAIL_USE_TLS',
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        'DEFAULT_FROM_EMAIL',
        'SERVER_EMAIL',
    ]
    
    for setting in settings_to_check:
        value = getattr(settings, setting, 'NOT SET')
        if setting == 'EMAIL_HOST_PASSWORD':
            display_value = '*' * len(str(value)) if value else 'NOT SET'
        else:
            display_value = value
        print(f"{setting}: {display_value}")
    
    print()
    
    # Check for common issues
    issues = []
    
    if not hasattr(settings, 'EMAIL_HOST_PASSWORD') or not settings.EMAIL_HOST_PASSWORD:
        issues.append("❌ EMAIL_HOST_PASSWORD is not set")
    
    if not hasattr(settings, 'EMAIL_HOST_USER') or not settings.EMAIL_HOST_USER:
        issues.append("❌ EMAIL_HOST_USER is not set")
    
    if settings.EMAIL_BACKEND != 'django.core.mail.backends.smtp.EmailBackend':
        issues.append(f"⚠️ Using non-SMTP backend: {settings.EMAIL_BACKEND}")
    
    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("✅ No configuration issues found")

def test_email_sending():
    """Test email sending functionality"""
    print("=" * 60)
    print("📧 TESTING EMAIL SENDING")
    print("=" * 60)
    
    test_email = "shyad.sdc@chettinad.com"
    
    try:
        print(f"Sending test email to {test_email}...")
        
        subject = 'Email Diagnostic Test'
        message = f"""
This is an email diagnostic test from the Data Management System.

Test Details:
- Timestamp: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
- From: {settings.DEFAULT_FROM_EMAIL}
- To: {test_email}
- Backend: {settings.EMAIL_BACKEND}

If you receive this email, the email system is working correctly.

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
        
        print("✅ Email sent successfully!")
        print("📬 Check your email inbox for the test message.")
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

def check_web_interface_issues():
    """Check for common web interface issues"""
    print("=" * 60)
    print("🌐 WEB INTERFACE ISSUES CHECK")
    print("=" * 60)
    
    print("Common causes of 'mail not send' in web interface:")
    print()
    print("1. 🔐 Authentication Issues:")
    print("   - User not logged in")
    print("   - Session expired")
    print("   - CSRF token missing or invalid")
    print()
    print("2. 📝 Form Submission Issues:")
    print("   - No records selected")
    print("   - Invalid email addresses")
    print("   - Missing required fields")
    print()
    print("3. 🖥️ Browser Issues:")
    print("   - JavaScript disabled")
    print("   - Network connectivity problems")
    print("   - Browser cache issues")
    print()
    print("4. 🐍 Django Issues:")
    print("   - Server not running")
    print("   - Database connection issues")
    print("   - Permission errors")
    print()
    print("5. 📧 Email Configuration Issues:")
    print("   - SMTP server down")
    print("   - Authentication failed")
    print("   - Rate limiting")
    print()

def provide_solutions():
    """Provide solutions for common issues"""
    print("=" * 60)
    print("🔧 SOLUTIONS FOR 'MAIL NOT SEND' ISSUES")
    print("=" * 60)
    
    print("STEP 1: Check Django Server")
    print("   - Ensure Django server is running: python manage.py runserver")
    print("   - Check server logs for errors")
    print()
    
    print("STEP 2: Verify Authentication")
    print("   - Make sure you're logged in to the system")
    print("   - Try logging out and logging back in")
    print()
    
    print("STEP 3: Test Email Configuration")
    print("   - Run: python test_email_setup.py")
    print("   - Run: python email_troubleshooter.py")
    print()
    
    print("STEP 4: Check Web Interface")
    print("   - Clear browser cache and cookies")
    print("   - Try a different browser")
    print("   - Check browser console for JavaScript errors")
    print()
    
    print("STEP 5: Verify Data")
    print("   - Ensure SPO records have valid email addresses")
    print("   - Check that records are selected before sending")
    print()
    
    print("STEP 6: Check Network")
    print("   - Verify internet connection")
    print("   - Check if SMTP server is accessible")
    print()

def main():
    """Main diagnostic function"""
    print("🔧 EMAIL DIAGNOSTIC TOOL")
    print("This tool will help identify the cause of 'mail not send' issues.")
    print()
    
    # Check Django server
    server_running = check_django_server()
    
    print()
    
    # Check email settings
    check_email_settings()
    
    print()
    
    # Test email sending
    email_working = test_email_sending()
    
    print()
    
    # Test endpoints if server is running
    if server_running:
        test_email_endpoints()
    
    print()
    
    # Check for web interface issues
    check_web_interface_issues()
    
    print()
    
    # Provide solutions
    provide_solutions()
    
    print("=" * 60)
    print("📋 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    if server_running and email_working:
        print("✅ Django server is running")
        print("✅ Email configuration is working")
        print()
        print("🔍 The issue is likely in the web interface:")
        print("   - Check browser console for errors")
        print("   - Verify you're logged in")
        print("   - Ensure records are selected")
        print("   - Check form submission")
    elif not server_running:
        print("❌ Django server is not running")
        print("   Solution: Start with 'python manage.py runserver'")
    elif not email_working:
        print("❌ Email configuration has issues")
        print("   Solution: Run 'python email_troubleshooter.py'")
    else:
        print("❌ Multiple issues detected")
        print("   Solution: Follow the troubleshooting steps above")

if __name__ == "__main__":
    main() 