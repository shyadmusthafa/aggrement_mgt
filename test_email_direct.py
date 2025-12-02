#!/usr/bin/env python3
"""
Direct test script to test email functionality by calling Django functions directly
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from dashboard.models import SPORent
from dashboard.views import generate_renewal_email_content
from django.core.mail import send_mail
from django.conf import settings

def test_email_directly():
    """Test email functionality directly using Django functions"""
    
    print("=" * 60)
    print("🧪 TESTING EMAIL FUNCTIONALITY DIRECTLY")
    print("=" * 60)
    
    # Get the SPO record with code '001'
    try:
        record = SPORent.objects.get(spo_code='001')
        print(f"✅ Found SPO record: {record.spo_name} ({record.spo_code})")
        print(f"   Email: {record.cfa_mail_id}")
        print(f"   Rental To Date: {record.rental_to_date}")
    except SPORent.DoesNotExist:
        print("❌ SPO record with code '001' not found")
        return
    
    # Test 1: Generate email content
    print("\n📝 Testing email content generation...")
    try:
        email_content = generate_renewal_email_content(record, "This is a test message")
        print("✅ Email content generated successfully")
        print(f"Content length: {len(email_content)} characters")
        print("First 200 characters:")
        print(email_content[:200] + "...")
    except Exception as e:
        print(f"❌ Failed to generate email content: {e}")
        return
    
    # Test 2: Test email sending
    print("\n📧 Testing email sending...")
    try:
        subject = f'SPO Rent Agreement Renewal Reminder - {record.spo_name}'
        
        # Send email
        send_mail(
            subject=subject,
            message=email_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[record.cfa_mail_id],
            fail_silently=False,
        )
        print("✅ Email sent successfully!")
        print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
        print(f"   To: {record.cfa_mail_id}")
        print(f"   Subject: {subject}")
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # Check email settings
        print("\n📋 Email settings check:")
        print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    print("\n" + "=" * 60)
    print("🎯 DIRECT TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_email_directly() 