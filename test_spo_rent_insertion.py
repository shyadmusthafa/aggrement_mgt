#!/usr/bin/env python
"""
Test script to validate SPO Rent data insertion
"""
import os
import sys
import django
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_management.settings')
django.setup()

from dashboard.models import SPORent, MasState, MasStateBranch, MasDistrict, MasConstruction, MasPartner

def test_spo_rent_insertion():
    """Test SPO Rent data insertion with the provided payload"""
    
    # Test payload data
    payload_data = {
        'state': 7,
        'branch': 5,
        'district': 119,
        'district_code': 'TN26',
        'spo_code': 'E007',
        'spo_name': 'HINDUPUR SPO',
        'stru_grp': 'Road',
        'cfa_status': 'Active',
        'renewal_with': 'Agreement',
        'inception_date': '2025-05-22',
        'godown_address': 'H.No 21060188,Teachers Colony, Revenue Ward 21 Hindupur Andhra Pradesh - 515201',
        'owner_name': 'Geetha',
        'owner_contact_no': '9384148769',
        'owner_code': '3900200',
        'owner_address': 'H.No. 16-10-35, Tippukhan Street, Hindupur, Anantapur, Ap - 515201',
        'owner_gst': '37ACRPN5550H1Z5',
        'owner_pan': 'ACRPN5550H',
        'pin_code': '639004',
        'nature_of_construction': 2,
        'sale_organization': 'Chettinad',
        'stamp_no': '546161',
        'stamp_name': 'India',
        'partner_type': 3,
        'cfa_mail_id': 'ashwinsm66@gmail.com',
        'bank_account_name': 'Musthafa',
        'bank_account_no': '93001000000982',
        'bank_name': 'IOB',
        'bank_branch_name': 'Adyar',
        'bank_ifsc_code': 'SBIN0000845',
        'destination_code': '25',
        'office_sqft': '25',
        'open_space_sqft': '25',
        'total_space': '25',
        'capacity': '25',
        'rental_from_date': '2025-08-13',
        'rental_to_date': '2025-12-27',
        'days_count': 137,
        'security_deposit_paid': '51566',
        'security_deposit_doc': '2222000',
        'rent_pm': '1500',
        'yearly_hike_percent': '12',
        'latitude': '55',
        'longitude': '55',
        'remarks': 'test',
        'status': 'Active'
    }
    
    print("=== SPO Rent Data Validation Test ===")
    print(f"Payload data: {len(payload_data)} fields")
    
    # Check if related records exist
    try:
        state = MasState.objects.get(id=payload_data['state'])
        print(f"✓ State found: {state.state_name}")
    except MasState.DoesNotExist:
        print(f"✗ State with ID {payload_data['state']} not found")
        return False
    
    try:
        branch = MasStateBranch.objects.get(id=payload_data['branch'])
        print(f"✓ Branch found: {branch.state_branch_name}")
    except MasStateBranch.DoesNotExist:
        print(f"✗ Branch with ID {payload_data['branch']} not found")
        return False
    
    try:
        district = MasDistrict.objects.get(id=payload_data['district'])
        print(f"✓ District found: {district.name}")
    except MasDistrict.DoesNotExist:
        print(f"✗ District with ID {payload_data['district']} not found")
        return False
    
    try:
        construction = MasConstruction.objects.get(id=payload_data['nature_of_construction'])
        print(f"✓ Construction type found: {construction.name}")
    except MasConstruction.DoesNotExist:
        print(f"✗ Construction type with ID {payload_data['nature_of_construction']} not found")
        return False
    
    try:
        partner = MasPartner.objects.get(id=payload_data['partner_type'])
        print(f"✓ Partner type found: {partner.name}")
    except MasPartner.DoesNotExist:
        print(f"✗ Partner type with ID {payload_data['partner_type']} not found")
        return False
    
    # Check choice field values
    valid_stru_grp = ['Road', 'Rail', 'TDP', 'Others']
    if payload_data['stru_grp'] not in valid_stru_grp:
        print(f"✗ Invalid stru_grp: {payload_data['stru_grp']}. Valid values: {valid_stru_grp}")
        return False
    else:
        print(f"✓ Valid stru_grp: {payload_data['stru_grp']}")
    
    valid_cfa_status = ['Active', 'Inactive', 'Suspended', 'Terminated']
    if payload_data['cfa_status'] not in valid_cfa_status:
        print(f"✗ Invalid cfa_status: {payload_data['cfa_status']}. Valid values: {valid_cfa_status}")
        return False
    else:
        print(f"✓ Valid cfa_status: {payload_data['cfa_status']}")
    
    valid_renewal_with = ['Agreement', 'Renewal']
    if payload_data['renewal_with'] not in valid_renewal_with:
        print(f"✗ Invalid renewal_with: {payload_data['renewal_with']}. Valid values: {valid_renewal_with}")
        return False
    else:
        print(f"✓ Valid renewal_with: {payload_data['renewal_with']}")
    
    valid_sale_organization = ['Chettinad', 'Anjani']
    if payload_data['sale_organization'] not in valid_sale_organization:
        print(f"✗ Invalid sale_organization: {payload_data['sale_organization']}. Valid values: {valid_sale_organization}")
        return False
    else:
        print(f"✓ Valid sale_organization: {payload_data['sale_organization']}")
    
    valid_status = ['Active', 'Inactive', 'Suspended', 'Terminated']
    if payload_data['status'] not in valid_status:
        print(f"✗ Invalid status: {payload_data['status']}. Valid values: {valid_status}")
        return False
    else:
        print(f"✓ Valid status: {payload_data['status']}")
    
    # Check date fields
    try:
        inception_date = datetime.strptime(payload_data['inception_date'], '%Y-%m-%d').date()
        print(f"✓ Valid inception_date: {inception_date}")
    except ValueError:
        print(f"✗ Invalid inception_date format: {payload_data['inception_date']}")
        return False
    
    try:
        rental_from_date = datetime.strptime(payload_data['rental_from_date'], '%Y-%m-%d').date()
        print(f"✓ Valid rental_from_date: {rental_from_date}")
    except ValueError:
        print(f"✗ Invalid rental_from_date format: {payload_data['rental_from_date']}")
        return False
    
    try:
        rental_to_date = datetime.strptime(payload_data['rental_to_date'], '%Y-%m-%d').date()
        print(f"✓ Valid rental_to_date: {rental_to_date}")
    except ValueError:
        print(f"✗ Invalid rental_to_date format: {payload_data['rental_to_date']}")
        return False
    
    # Check numeric fields
    try:
        days_count = int(payload_data['days_count'])
        print(f"✓ Valid days_count: {days_count}")
    except ValueError:
        print(f"✗ Invalid days_count: {payload_data['days_count']}")
        return False
    
    try:
        security_deposit_paid = float(payload_data['security_deposit_paid'])
        print(f"✓ Valid security_deposit_paid: {security_deposit_paid}")
    except ValueError:
        print(f"✗ Invalid security_deposit_paid: {payload_data['security_deposit_paid']}")
        return False
    
    try:
        rent_pm = float(payload_data['rent_pm'])
        print(f"✓ Valid rent_pm: {rent_pm}")
    except ValueError:
        print(f"✗ Invalid rent_pm: {payload_data['rent_pm']}")
        return False
    
    try:
        yearly_hike_percent = float(payload_data['yearly_hike_percent'])
        print(f"✓ Valid yearly_hike_percent: {yearly_hike_percent}")
    except ValueError:
        print(f"✗ Invalid yearly_hike_percent: {payload_data['yearly_hike_percent']}")
        return False
    
    try:
        latitude = float(payload_data['latitude'])
        print(f"✓ Valid latitude: {latitude}")
    except ValueError:
        print(f"✗ Invalid latitude: {payload_data['latitude']}")
        return False
    
    try:
        longitude = float(payload_data['longitude'])
        print(f"✓ Valid longitude: {longitude}")
    except ValueError:
        print(f"✗ Invalid longitude: {payload_data['longitude']}")
        return False
    
    print("\n=== All validations passed! ===")
    print("Data can be inserted into SPORent table.")
    return True

if __name__ == '__main__':
    test_spo_rent_insertion()
