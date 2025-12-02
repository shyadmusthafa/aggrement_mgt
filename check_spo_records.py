#!/usr/bin/env python3
"""
Script to check existing SPO records and their email addresses
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from dashboard.models import SPORent

def check_spo_records():
    """Check existing SPO records and their email addresses"""
    
    print("=" * 60)
    print("📋 CHECKING SPO RECORDS")
    print("=" * 60)
    
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
        print("\n📧 Records with email addresses:")
        print("-" * 40)
        for record in records_with_email[:10]:  # Show first 10
            print(f"ID: {record.id}")
            print(f"SPO Code: {record.spo_code}")
            print(f"SPO Name: {record.spo_name}")
            print(f"Email: {record.cfa_mail_id}")
            print(f"Rental To Date: {record.rental_to_date}")
            print("-" * 20)
    else:
        print("\n❌ No records with email addresses found!")
        print("You need to add email addresses to SPO records to test email functionality.")
    
    # Check for specific SPO code '001'
    try:
        record_001 = SPORent.objects.get(spo_code='001')
        print(f"\n✅ Found SPO record with code '001':")
        print(f"   ID: {record_001.id}")
        print(f"   Name: {record_001.spo_name}")
        print(f"   Email: {record_001.cfa_mail_id or 'No email'}")
    except SPORent.DoesNotExist:
        print("\n❌ No SPO record found with code '001'")
    
    print("\n" + "=" * 60)
    print("🎯 CHECK COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    check_spo_records() 