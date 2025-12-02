#!/usr/bin/env python
"""
Test script for automatic mail trigger functionality
This script demonstrates how the system would automatically trigger emails 6 days before expiry
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.utils import timezone
from dashboard.models import SPORent

def test_auto_mail_trigger():
    """Test the automatic mail trigger logic"""
    print("=" * 60)
    print("🧪 TESTING AUTOMATIC MAIL TRIGGER FUNCTIONALITY")
    print("=" * 60)
    
    # Get current date
    today = timezone.now().date()
    target_date = today + timedelta(days=6)
    
    print(f"Current Date: {today}")
    print(f"Target Date (6 days from now): {target_date}")
    print(f"Looking for SPO Rent agreements expiring on: {target_date}")
    print()
    
    # Find SPO Rent records expiring in exactly 6 days
    expiring_records = SPORent.objects.filter(
        rental_to_date=target_date,
        status='Active',
        cfa_mail_id__isnull=False
    ).exclude(
        cfa_mail_id=''
    ).select_related('branch')
    
    print(f"Found {expiring_records.count()} records expiring on {target_date}")
    print()
    
    if expiring_records.exists():
        print("📋 RECORDS THAT WOULD TRIGGER AUTOMATIC EMAILS:")
        print("-" * 50)
        
        for i, record in enumerate(expiring_records, 1):
            print(f"{i}. SPO Code: {record.spo_code}")
            print(f"   SPO Name: {record.spo_name}")
            print(f"   Owner: {record.owner_name or 'N/A'}")
            print(f"   Branch: {record.branch.state_branch_name if record.branch else 'N/A'}")
            print(f"   Email: {record.cfa_mail_id}")
            print(f"   Expiry Date: {record.rental_to_date}")
            print(f"   Days Until Expiry: 6")
            print(f"   Status: {record.status}")
            print()
            
            # Simulate email content
            print("   📧 SIMULATED EMAIL CONTENT:")
            print("   " + "-" * 40)
            print(f"   To: {record.cfa_mail_id}")
            print(f"   Subject: SPO Rent Agreement Renewal Reminder - {record.spo_code}")
            print(f"   Message: Agreement for {record.spo_name} expires in 6 days")
            print("   " + "-" * 40)
            print()
    else:
        print("✅ No records found expiring in exactly 6 days")
        print()
        
        # Show some sample records for demonstration
        print("📊 SAMPLE RECORDS FOR REFERENCE:")
        print("-" * 40)
        
        sample_records = SPORent.objects.filter(
            status='Active',
            cfa_mail_id__isnull=False
        ).exclude(
            cfa_mail_id=''
        ).select_related('branch')[:5]
        
        for i, record in enumerate(sample_records, 1):
            if record.rental_to_date:
                days_until_expiry = (record.rental_to_date - today).days
                print(f"{i}. {record.spo_code} - {record.spo_name}")
                print(f"   Expires: {record.rental_to_date} ({days_until_expiry} days)")
                print(f"   Email: {record.cfa_mail_id}")
                print()
    
    # Test different scenarios
    print("🔍 TESTING DIFFERENT SCENARIOS:")
    print("-" * 40)
    
    # Records expiring in next 7 days
    next_week = today + timedelta(days=7)
    upcoming_records = SPORent.objects.filter(
        rental_to_date__lte=next_week,
        rental_to_date__gte=today,
        status='Active',
        cfa_mail_id__isnull=False
    ).exclude(
        cfa_mail_id=''
    ).order_by('rental_to_date')
    
    print(f"Records expiring in next 7 days: {upcoming_records.count()}")
    
    for record in upcoming_records:
        days_left = (record.rental_to_date - today).days
        trigger_status = "🔥 AUTO-TRIGGER" if days_left <= 6 else "⏰ MANUAL ONLY"
        print(f"   {record.spo_code}: {days_left} days left - {trigger_status}")
    
    print()
    
    # Records that expired
    expired_records = SPORent.objects.filter(
        rental_to_date__lt=today,
        status='Active',
        cfa_mail_id__isnull=False
    ).exclude(
        cfa_mail_id=''
    ).order_by('-rental_to_date')[:5]
    
    print(f"Recently expired records: {expired_records.count()}")
    
    for record in expired_records:
        days_expired = (today - record.rental_to_date).days
        print(f"   {record.spo_code}: Expired {days_expired} days ago")
    
    print()
    print("=" * 60)
    print("✅ AUTOMATIC MAIL TRIGGER TEST COMPLETED")
    print("=" * 60)
    
    # Summary
    total_with_email = SPORent.objects.exclude(
        cfa_mail_id__isnull=True
    ).exclude(
        cfa_mail_id=''
    ).count()
    
    total_active = SPORent.objects.filter(status='Active').count()
    
    print(f"📊 SUMMARY:")
    print(f"   Total SPO Records: {SPORent.objects.count()}")
    print(f"   Records with Email: {total_with_email}")
    print(f"   Active Records: {total_active}")
    print(f"   Ready for Auto-Trigger: {expiring_records.count()}")
    
    if expiring_records.exists():
        print(f"\n🚀 RECOMMENDATION:")
        print(f"   Run automatic mail trigger for {expiring_records.count()} records")
        print(f"   Command: python manage.py send_scheduled_reminders")
    else:
        print(f"\n✅ STATUS:")
        print(f"   No automatic triggers needed at this time")

if __name__ == "__main__":
    test_auto_mail_trigger()
