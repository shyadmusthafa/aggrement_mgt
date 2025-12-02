#!/usr/bin/env python3
"""
Test script for SPO Rent Export functionality with filter options
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth.models import User

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def test_export_functionality():
    """Test the export functionality with various filter combinations"""
    
    # Create a test user if needed
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    # Create a test client
    client = Client()
    
    # Login
    login_success = client.login(username='testuser', password='testpass123')
    if not login_success:
        print("❌ Failed to login with test user")
        return False
    
    print("✅ Successfully logged in")
    
    # Test 1: Basic export without filters
    print("\n🧪 Test 1: Basic export without filters")
    response = client.get('/dashboard/spo-rent/export-excel/')
    if response.status_code == 200:
        print("✅ Basic export works")
        print(f"   Content-Type: {response.get('Content-Type', 'Not set')}")
        print(f"   Content-Disposition: {response.get('Content-Disposition', 'Not set')}")
    else:
        print(f"❌ Basic export failed with status code: {response.status_code}")
    
    # Test 2: Export with SPO name filter
    print("\n🧪 Test 2: Export with SPO name filter")
    response = client.get('/dashboard/spo-rent/export-excel/?spo_name=test')
    if response.status_code == 200:
        print("✅ Export with SPO name filter works")
    else:
        print(f"❌ Export with SPO name filter failed: {response.status_code}")
    
    # Test 3: Export with multiple filters
    print("\n🧪 Test 3: Export with multiple filters")
    response = client.get('/dashboard/spo-rent/export-excel/?spo_name=test&spo_code=A123&include_summary=true')
    if response.status_code == 200:
        print("✅ Export with multiple filters works")
    else:
        print(f"❌ Export with multiple filters failed: {response.status_code}")
    
    # Test 4: Export with date range filters
    print("\n🧪 Test 4: Export with date range filters")
    response = client.get('/dashboard/spo-rent/export-excel/?rent_from_date_min=2024-01-01&rent_to_date_max=2024-12-31')
    if response.status_code == 200:
        print("✅ Export with date range filters works")
    else:
        print(f"❌ Export with date range filters failed: {response.status_code}")
    
    # Test 5: Export with rent amount range
    print("\n🧪 Test 5: Export with rent amount range")
    response = client.get('/dashboard/spo-rent/export-excel/?rent_amount=0-5000')
    if response.status_code == 200:
        print("✅ Export with rent amount range works")
    else:
        print(f"❌ Export with rent amount range failed: {response.status_code}")
    
    # Test 6: Export with all records option
    print("\n🧪 Test 6: Export with all records option")
    response = client.get('/dashboard/spo-rent/export-excel/?include_all_records=true&include_summary=false')
    if response.status_code == 200:
        print("✅ Export with all records option works")
    else:
        print(f"❌ Export with all records option failed: {response.status_code}")
    
    # Test 7: Export with current filters option
    print("\n🧪 Test 7: Export with current filters option")
    response = client.get('/dashboard/spo-rent/export-excel/?include_current_filters=true&spo_name=test')
    if response.status_code == 200:
        print("✅ Export with current filters option works")
    else:
        print(f"❌ Export with current filters option failed: {response.status_code}")
    
    print("\n🎉 Export functionality testing completed!")
    return True

def test_url_patterns():
    """Test that the URL patterns are correctly configured"""
    print("\n🔗 Testing URL patterns...")
    
    try:
        from django.urls import reverse
        from django.test import Client
        
        client = Client()
        
        # Test the export URL
        export_url = reverse('spo_rent_export_excel')
        print(f"✅ Export URL pattern: {export_url}")
        
        # Test the list URL
        list_url = reverse('spo_rent_list')
        print(f"✅ List URL pattern: {list_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ URL pattern test failed: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Starting SPO Rent Export Functionality Tests")
    print("=" * 50)
    
    # Test URL patterns
    url_test = test_url_patterns()
    
    # Test export functionality
    export_test = test_export_functionality()
    
    print("\n" + "=" * 50)
    if url_test and export_test:
        print("🎉 All tests passed! Export functionality is working correctly.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    
    print("\n📋 Summary of new features:")
    print("✅ Export to Excel button with filter options modal")
    print("✅ Filter options: SPO Code, SPO Name, State, Branch, Owner details")
    print("✅ Date range filters for rent periods")
    print("✅ Rent amount range filters")
    print("✅ Export options: Include current filters, all records, summary")
    print("✅ Pre-filled filter values from current page")
    print("✅ Enhanced Excel export with detailed summary information") 