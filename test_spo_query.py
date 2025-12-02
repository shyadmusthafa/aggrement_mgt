#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from dashboard.models import SPORent

# Test the same query used in the view
records = SPORent.objects.exclude(
    cfa_mail_id__isnull=True
).exclude(
    cfa_mail_id=''
).select_related('state', 'branch')

print(f"Records found with email addresses: {records.count()}")

# Show all records
for record in records:
    print(f"SPO Code: {record.spo_code}")
    print(f"SPO Name: {record.spo_name}")
    print(f"Email: {record.cfa_mail_id}")
    print(f"State: {record.state.state_name if record.state else 'N/A'}")
    print(f"Status: {record.status}")
    print("-" * 50) 