#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from dashboard.models import SPORent

# Update existing records
records = SPORent.objects.all()
for record in records:
    # Set default values for new fields
    if not record.cfa_name:
        record.cfa_name = record.owner_name or 'Default CFA'
    
    if not record.cfa_mail_id:
        record.cfa_mail_id = 'default@example.com'
    
    if not record.status or record.status == 1:
        record.status = 'Active'
    
    if not record.cfa_address:
        record.cfa_address = 'Default Address'
    
    if not record.owner_contact_no:
        record.owner_contact_no = '0000000000'
    
    if not record.gst_no:
        record.gst_no = 'DEFAULTGST'
    
    if not record.pan_no:
        record.pan_no = 'DEFAULTPAN'
    
    if not record.bank_account_name:
        record.bank_account_name = record.owner_name or 'Default Account'
    
    if not record.bank_branch_name:
        record.bank_branch_name = 'Default Branch'
    
    if not record.destination_code:
        record.destination_code = 'DEFAULT'
    
    if not record.security_deposit_rs:
        record.security_deposit_rs = 0.00
    
    if not record.security_deposit_doc_ref_dd:
        record.security_deposit_doc_ref_dd = 'Default Reference'
    
    record.save()
    print(f"Updated record {record.id}: {record.spo_name}")

print(f"Successfully updated {records.count()} records!") 