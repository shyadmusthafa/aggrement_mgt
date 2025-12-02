#!/usr/bin/env python
"""
Test UI Email Functionality
This script tests the email functionality that should work from the web UI
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

# Import models
from dashboard.models import SPORent

def check_spo_records():
    """Check SPO records in the database"""
    print("=" * 60)
    print("📊 CHECKING SPO RECORDS IN DATABASE")
    print("=" * 60)
    
    try:
        # Get all SPO records
        all_records = SPORent.objects.all()
        print(f"Total SPO records: {all_records.count()}")
        
        # Get records with email addresses
        records_with_email = SPORent.objects.exclude(
            cfa_mail_id__isnull=True
        ).exclude(
            cfa_mail_id=''
        )
        print(f"Records with email addresses: {records_with_email.count()}")
        
        if records_with_email.exists():
            print("\nRecords with email addresses:")
            for record in records_with_email[:5]:  # Show first 5
                print(f"  - SPO Code: {record.spo_code}")
                print(f"    SPO Name: {record.spo_name}")
                print(f"    Email: {record.cfa_mail_id}")
                print(f"    Status: {record.status}")
                print()
        else:
            print("❌ No SPO records with email addresses found!")
            print("This is why emails are not sending from the UI.")
            print()
            print("To fix this:")
            print("1. Add SPO records with valid email addresses")
            print("2. Make sure the 'cfa_mail_id' field is filled")
            print("3. Check that email addresses are valid")
        
        return records_with_email.exists()
        
    except Exception as e:
        print(f"❌ Error checking SPO records: {str(e)}")
        return False

def test_ui_email_sending():
    """Test the same email sending logic used in the UI"""
    print("=" * 60)
    print("📧 TESTING UI EMAIL SENDING")
    print("=" * 60)
    
    try:
        # Get a record with email address
        record = SPORent.objects.exclude(
            cfa_mail_id__isnull=True
        ).exclude(
            cfa_mail_id=''
        ).first()
        
        if not record:
            print("❌ No SPO records with email addresses found!")
            print("Cannot test email sending without valid records.")
            return False
        
        print(f"Testing with record: {record.spo_code} ({record.cfa_mail_id})")
        
        # Test the same logic used in views.py
        email_type = 'renewal'
        custom_message = 'This is a test email from the UI.'
        
        # Generate email content (simplified version)
        if email_type == 'renewal':
            subject = f'SPO Rent Agreement Renewal Reminder - {record.spo_name}'
            message = f"""
Dear {record.spo_name},

This is a reminder about your SPO Rent Agreement renewal.

Agreement Details:
- SPO Code: {record.spo_code}
- Current Status: {record.status}
- Agreement Period: {record.rental_from_date} to {record.rental_to_date}

{custom_message if custom_message else 'Please contact our support team for any assistance.'}

Best regards,
Chettinad Software Center
Data Management Team
            """.strip()
        
        # Send email using the same method as in views.py
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[record.cfa_mail_id],
            fail_silently=False,
        )
        
        print("✅ UI email test successful!")
        print(f"📬 Email sent to: {record.cfa_mail_id}")
        print(f"📧 Subject: {subject}")
        return True
        
    except Exception as e:
        print(f"❌ UI email test failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

def create_test_record():
    """Create a test SPO record with email address"""
    print("=" * 60)
    print("➕ CREATING TEST SPO RECORD")
    print("=" * 60)
    
    try:
        # Check if test record already exists
        test_record = SPORent.objects.filter(spo_code='TEST001').first()
        if test_record:
            print("Test record already exists:")
            print(f"  SPO Code: {test_record.spo_code}")
            print(f"  Email: {test_record.cfa_mail_id}")
            return True
        
        # Create test record
        test_record = SPORent.objects.create(
            spo_code='TEST001',
            spo_name='Test SPO for Email',
            cfa_mail_id='shyad.sdc@chettinad.com',
            status='Active',
            rental_from_date='2025-01-01',
            rental_to_date='2025-12-31',
            rent_pm=5000,
            owner_name='Test Owner',
            owner_phone='1234567890',
            owner_address='Test Address'
        )
        
        print("✅ Test SPO record created successfully!")
        print(f"  SPO Code: {test_record.spo_code}")
        print(f"  SPO Name: {test_record.spo_name}")
        print(f"  Email: {test_record.cfa_mail_id}")
        print(f"  Status: {test_record.status}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating test record: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🔧 TESTING UI EMAIL FUNCTIONALITY")
    print("This script tests the email functionality that should work from the web UI.")
    print()
    
    # Check existing records
    has_records = check_spo_records()
    
    print()
    
    # If no records, create a test record
    if not has_records:
        print("Creating a test record to enable email testing...")
        create_test_record()
        print()
    
    # Test UI email sending
    ui_test_success = test_ui_email_sending()
    
    print()
    print("=" * 60)
    print("📋 UI EMAIL TEST RESULTS")
    print("=" * 60)
    
    if ui_test_success:
        print("🎉 UI EMAIL TEST PASSED!")
        print("✅ Email functionality is working correctly")
        print("✅ The issue is not with the email system")
        print()
        print("🔍 If emails are still not sending from the web UI:")
        print("1. Make sure you're logged in to the system")
        print("2. Check that you've selected records before sending")
        print("3. Verify the form is being submitted correctly")
        print("4. Check browser console for JavaScript errors")
        print("5. Check Django server logs for any errors")
    else:
        print("❌ UI EMAIL TEST FAILED")
        print("The email system has issues that need to be fixed.")
    
    print()
    print("📝 NEXT STEPS:")
    print("1. Go to: http://127.0.0.1:8000/dashboard/mail-reminder/spo-rent/")
    print("2. Select one or more records")
    print("3. Choose email type and add custom message")
    print("4. Click 'Send Email to Selected Records'")
    print("5. Check if you receive the emails")

if __name__ == "__main__":
    main() 