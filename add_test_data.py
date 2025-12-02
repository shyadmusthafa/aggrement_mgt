#!/usr/bin/env python
import os
import django
from datetime import date, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from dashboard.models import SPORent, MasState, MasStateBranch

# Check if we have states
states = MasState.objects.all()
if not states.exists():
    print("No states found. Creating sample states...")
    # Create sample states
    karnataka = MasState.objects.create(
        state_name="Karnataka",
        state_code="KA",
        status=1
    )
    tamil_nadu = MasState.objects.create(
        state_name="Tamil Nadu",
        state_code="TN",
        status=1
    )
    print("Created sample states")
else:
    print(f"Found {states.count()} states")
    karnataka = states.first()  # Use first available state

# Check if we have branches
branches = MasStateBranch.objects.all()
if not branches.exists():
    print("No branches found. Creating sample branches...")
    # Create sample branch
    branch = MasStateBranch.objects.create(
        state=karnataka,
        state_branch_name="Bangalore Branch",
        state_branch_code="BLR001"
    )
    print("Created sample branch")
else:
    print(f"Found {branches.count()} branches")
    branch = branches.first()  # Use first available branch

# Check existing SPO Rent records
existing_records = SPORent.objects.all()
print(f"Found {existing_records.count()} existing SPO Rent records")

# Add test SPO Rent record if none exist
if not existing_records.exists():
    print("Creating test SPO Rent record...")
    
    # Create test SPO Rent record
    test_record = SPORent.objects.create(
        state=karnataka,
        branch=branch,
        district_code="BLR001",
        spo_code="TEST001",
        spo_name="Test SPO Rent",
        stru_grp="Road",
        cfa_status="Active",
        inception_date=date.today() - timedelta(days=365),
        owner_name="Test Owner",
        owner_contact_no="9876543210",
        cfa_mail_id="test@example.com",  # This is the email field
        bank_account_name="Test Bank Account",
        bank_account_no="1234567890",
        bank_name="Test Bank",
        bank_branch_name="Test Branch",
        bank_ifsc_code="TEST0001234",
        destination_code="TEST001",
        office_sqft="1000",
        open_space_sqft="500",
        total_space="1500",
        rental_from_date=date.today() - timedelta(days=365),
        rental_to_date=date.today() + timedelta(days=30),  # Expiring soon
        security_deposit_paid=50000.00,
        security_deposit_doc="Test Doc",
        rent_pm=10000.00,
        yearly_hike_percent=5.00,
        remarks="Test record for email functionality",
        status="Active"
    )
    print(f"Created test SPO Rent record: {test_record.spo_code}")
else:
    print("SPO Rent records already exist")

# Check records with email addresses
records_with_email = SPORent.objects.exclude(
    cfa_mail_id__isnull=True
).exclude(
    cfa_mail_id=''
)

print(f"\nRecords with email addresses: {records_with_email.count()}")
for record in records_with_email:
    print(f"- SPO Code: {record.spo_code}, Email: {record.cfa_mail_id}")

print("\nTest data setup complete!") 