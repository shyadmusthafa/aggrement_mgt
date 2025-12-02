#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from dashboard.models import SPORent
from datetime import date, datetime

def test_spo_creation():
    print("Testing SPO Rent creation...")
    
    # Check if we can query existing records
    try:
        count = SPORent.objects.count()
        print(f"Current SPO Rent records: {count}")
    except Exception as e:
        print(f"Error querying SPO Rent records: {e}")
        return
    
    # Try to create a test record
    try:
        test_record = SPORent.objects.create(
            state='Test State',
            branch_name='Test Branch',
            district_code='TEST01',
            district_name='Test District',
            spo_code='TEST001',
            spo_name='Test SPO',
            stru_grp='Others',
            spo_status='Active',
            inception_date=date.today(),
            godown_address='Test Address',
            owner_code='OWN001',
            owner_name='Test Owner',
            owner_address='Test Owner Address',
            owner_contact='1234567890',
    
            owner_gst='GST123456789',
            owner_pan='PAN123456789',
            bank_account_name='Test Bank Account',
            bank_account_no='1234567890',
            bank_name='Test Bank',
            branch_name_bank='Test Bank Branch',
            bank_ifsc_code='TEST0001234',
            depot_sqft=1000.00,
            office_sqft=500.00,
            open_space_sqft=2000.00,
            total_space=3500.00,
            capacity=5000.00,
            from_date=date.today(),
            to_date=date.today(),
            days_count=1,
            security_deposit_paid=50000.00,
            security_deposit_doc='Test Doc',
            rent_pm=25000.00,
            yearly_hike_percent=5.00,
            latitude='28.7041',
            longitude='77.1025',
            vacation_letter='Test Letter',
            remarks='Test remarks',
            status=1
        )
        print(f"Successfully created test record with ID: {test_record.id}")
        
        # Clean up - delete the test record
        test_record.delete()
        print("Test record deleted successfully")
        
    except Exception as e:
        print(f"Error creating test record: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_spo_creation() 