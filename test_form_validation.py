#!/usr/bin/env python3
"""
Test script to verify SPO Rent form validation
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from dashboard.forms import SPORentForm
from dashboard.models import MasState, MasStateBranch

def test_form_validation():
    """Test the SPO Rent form validation"""
    
    print("Testing SPO Rent Form Validation...")
    print("=" * 50)
    
    # Test 1: Empty form (should have validation errors)
    print("\n1. Testing empty form:")
    form = SPORentForm()
    print(f"Form is valid: {form.is_valid()}")
    if not form.is_valid():
        print("Validation errors:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
    
    # Test 2: Form with minimal required data
    print("\n2. Testing form with minimal required data:")
    
    # Get some sample data for required fields
    try:
        state = MasState.objects.first()
        branch = MasStateBranch.objects.first()
        
        if state and branch:
            data = {
                'sale_organization': 'Chettinad',
                'spo_code': 'A001',
                'state': state.id,
                'branch': branch.id,
                'spo_name': 'Test SPO',
                'stru_grp': 'Road',
                'cfa_status': 'Active',
                'inception_date': '2025-01-01',
            }
            
            form = SPORentForm(data)
            print(f"Form is valid: {form.is_valid()}")
            if not form.is_valid():
                print("Validation errors:")
                for field, errors in form.errors.items():
                    print(f"  {field}: {errors}")
            else:
                print("✓ Form validation passed!")
        else:
            print("⚠ No state or branch data available for testing")
            
    except Exception as e:
        print(f"Error during testing: {e}")
    
    # Test 3: Form with invalid SPO code format
    print("\n3. Testing form with invalid SPO code format:")
    if state and branch:
        data = {
            'sale_organization': 'Chettinad',
            'spo_code': 'INVALID',  # Invalid format
            'state': state.id,
            'branch': branch.id,
            'spo_name': 'Test SPO',
            'stru_grp': 'Road',
            'cfa_status': 'Active',
            'inception_date': '2025-01-01',
        }
        
        form = SPORentForm(data)
        print(f"Form is valid: {form.is_valid()}")
        if not form.is_valid():
            print("Validation errors:")
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
    
    print("\n" + "=" * 50)
    print("Form validation testing completed!")

if __name__ == "__main__":
    test_form_validation()
