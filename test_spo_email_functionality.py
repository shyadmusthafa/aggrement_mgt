#!/usr/bin/env python
"""
Test script to verify SPO email functionality
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail
from dashboard.models import SPORent

def test_spo_email_functionality():
    """Test the SPO email functionality"""
    print("=" * 70)
    print("🔧 TESTING SPO EMAIL FUNCTIONALITY")
    print("=" * 70)
    
    # Get SPO records with email addresses
    records = SPORent.objects.exclude(
        cfa_mail_id__isnull=True
    ).exclude(
        cfa_mail_id=''
    ).select_related('state', 'branch')
    
    print(f"Found {records.count()} SPO records with email addresses")
    
    if not records.exists():
        print("❌ No SPO records with email addresses found!")
        print("Please add some SPO records with email addresses first.")
        return False
    
    # Test with the first record
    test_record = records.first()
    print(f"\nTesting with SPO record:")
    print(f"  - SPO Code: {test_record.spo_code}")
    print(f"  - SPO Name: {test_record.spo_name}")
    print(f"  - Email: {test_record.cfa_mail_id}")
    print(f"  - Status: {test_record.status}")
    
    # Test email sending
    try:
        subject = f'Test Email - SPO Rent Agreement - {test_record.spo_name}'
        message = f"""
Dear {test_record.owner_name or 'Valued Customer'},

This is a test email from the Data Management System for SPO Rent Agreement.

Agreement Details:
- SPO Code: {test_record.spo_code}
- SPO Name: {test_record.spo_name}
- Current Agreement Period: {test_record.rental_from_date} to {test_record.rental_to_date}
- Monthly Rent: ₹{test_record.rent_pm or 'N/A'}
- Security Deposit: ₹{test_record.security_deposit_paid or 'N/A'}

This is a test email to verify the email functionality is working correctly.

Best regards,
Chettinad Software Center
Data Management Team
        """.strip()
        
        print(f"\n📧 Sending test email to {test_record.cfa_mail_id}...")
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_record.cfa_mail_id],
            fail_silently=False,
        )
        
        print("✅ Test email sent successfully!")
        print(f"📬 Check the inbox for: {test_record.cfa_mail_id}")
        print("📁 Also check the spam/junk folder")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {str(e)}")
        return False

def show_spo_records():
    """Show all SPO records with email addresses"""
    print("\n" + "=" * 70)
    print("📋 SPO RECORDS WITH EMAIL ADDRESSES")
    print("=" * 70)
    
    records = SPORent.objects.exclude(
        cfa_mail_id__isnull=True
    ).exclude(
        cfa_mail_id=''
    ).select_related('state', 'branch')
    
    if not records.exists():
        print("No SPO records with email addresses found.")
        return
    
    for i, record in enumerate(records, 1):
        print(f"{i}. SPO Code: {record.spo_code}")
        print(f"   SPO Name: {record.spo_name}")
        print(f"   Email: {record.cfa_mail_id}")
        print(f"   Status: {record.status}")
        print(f"   State: {record.state.state_name if record.state else 'N/A'}")
        print()

if __name__ == "__main__":
    print("🔧 SPO EMAIL FUNCTIONALITY TEST")
    print("This script will test the SPO email functionality.")
    print()
    
    # Show available records
    show_spo_records()
    
    # Test email functionality
    if test_spo_email_functionality():
        print("\n🎉 SPO EMAIL FUNCTIONALITY IS WORKING!")
        print("The email system is ready to send SPO rent reminders.")
    else:
        print("\n❌ SPO EMAIL FUNCTIONALITY TEST FAILED")
        print("Please check the error messages above.") 