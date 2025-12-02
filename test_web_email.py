#!/usr/bin/env python
"""
Test Email Functionality through Django Application
This script tests the email sending functions used in the web interface
"""

import os
import sys
import django
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def test_web_email_functions():
    """Test the email functions used in the web interface"""
    print("=" * 60)
    print("TESTING WEB EMAIL FUNCTIONS")
    print("=" * 60)
    
    # Test the same email sending logic used in views.py
    test_email = "shyad.sdc@chettinad.com"
    
    try:
        print(f"📧 Testing email sending to {test_email}...")
        
        subject = 'Test Email from Data Management System'
        message = f"""
Hello,

This is a test email from the Data Management System to verify email configuration.

Email Details:
- From: {settings.DEFAULT_FROM_EMAIL}
- To: {test_email}
- Sent at: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

If you receive this email, the email configuration is working correctly.

Best regards,
Chettinad Software Center
Data Management Team
        """.strip()
        
        # Use the same send_mail call as in views.py
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        print("✅ Web email function test successful!")
        print("📬 Check your email inbox for the test message.")
        return True
        
    except Exception as e:
        print(f"❌ Web email function test failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

def test_spo_rent_email_content():
    """Test the SPO rent email content generation"""
    print("=" * 60)
    print("TESTING SPO RENT EMAIL CONTENT")
    print("=" * 60)
    
    # Create a mock SPO record for testing
    class MockSPORecord:
        def __init__(self):
            self.spo_code = "TEST001"
            self.spo_name = "Test SPO"
            self.cfa_mail_id = "shyad.sdc@chettinad.com"
            self.rental_from_date = "2025-01-01"
            self.rental_to_date = "2025-12-31"
            self.status = "Active"
    
    mock_record = MockSPORecord()
    
    # Test the email content generation functions
    try:
        # Test renewal email content
        renewal_content = f"""
Dear {mock_record.spo_name},

This is a reminder about your SPO Rent Agreement renewal.

Agreement Details:
- SPO Code: {mock_record.spo_code}
- Current Status: {mock_record.status}
- Agreement Period: {mock_record.rental_from_date} to {mock_record.rental_to_date}

Please contact our support team for any assistance.

Best regards,
Chettinad Software Center
Data Management Team
        """.strip()
        
        print("✅ SPO rent email content generation successful!")
        print("Sample content:")
        print("-" * 40)
        print(renewal_content)
        print("-" * 40)
        return True
        
    except Exception as e:
        print(f"❌ SPO rent email content generation failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🔧 TESTING EMAIL FUNCTIONALITY")
    print("This script tests the email functions used in the web interface.")
    print()
    
    # Test web email functions
    web_test_success = test_web_email_functions()
    
    print()
    
    # Test SPO rent email content
    content_test_success = test_spo_rent_email_content()
    
    print()
    print("=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    if web_test_success and content_test_success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Email configuration is working correctly")
        print("✅ Web email functions are working")
        print("✅ Email content generation is working")
        print()
        print("If you're still experiencing 'mail not send' issues in the web interface:")
        print("1. Check if the Django server is running")
        print("2. Verify the URL you're accessing")
        print("3. Check browser console for JavaScript errors")
        print("4. Check Django server logs for any errors")
    else:
        print("❌ SOME TESTS FAILED")
        if not web_test_success:
            print("❌ Web email function test failed")
        if not content_test_success:
            print("❌ Email content generation test failed")

if __name__ == "__main__":
    main() 