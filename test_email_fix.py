#!/usr/bin/env python3
"""
Test script to verify email sending functionality after the fix
"""

import requests
import json

def test_email_sending():
    """Test the email sending functionality"""
    
    # Test data
    test_data = {
        'spo_code': '001',  # Use an existing SPO code
        'email': 'test@example.com',
        'reminder_type': 'renewal'
    }
    
    print("=" * 60)
    print("🧪 TESTING EMAIL SENDING FUNCTIONALITY")
    print("=" * 60)
    
    # Test 1: Check if server is running
    try:
        response = requests.get('http://127.0.0.1:8000/dashboard/mail-reminder/', timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and mail reminder page is accessible")
        else:
            print(f"❌ Server responded with status code: {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the Django server is running on http://127.0.0.1:8000")
        return
    
    # Test 2: Test email sending endpoint
    try:
        response = requests.post(
            'http://127.0.0.1:8000/dashboard/mail-reminder/spo-rent/send-email/',
            headers={
                'Content-Type': 'application/json',
                'X-CSRFToken': 'test-token'  # This will be handled by the view
            },
            data=json.dumps(test_data),
            timeout=10
        )
        
        print(f"📧 Email endpoint response status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"📧 Response: {result}")
                
                if result.get('success'):
                    print("✅ Email sending test completed successfully!")
                else:
                    print(f"⚠️ Email sending failed: {result.get('message', 'Unknown error')}")
            except json.JSONDecodeError:
                print("⚠️ Response is not JSON format")
                print(f"Response content: {response.text[:200]}...")
        else:
            print(f"❌ Email endpoint returned error status: {response.status_code}")
            print(f"Response content: {response.text[:200]}...")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing email endpoint: {e}")
    
    # Test 3: Test with invalid SPO code
    print("\n" + "=" * 40)
    print("Testing with invalid SPO code...")
    
    invalid_data = {
        'spo_code': 'INVALID999',
        'email': 'test@example.com',
        'reminder_type': 'renewal'
    }
    
    try:
        response = requests.post(
            'http://127.0.0.1:8000/dashboard/mail-reminder/spo-rent/send-email/',
            headers={
                'Content-Type': 'application/json',
                'X-CSRFToken': 'test-token'
            },
            data=json.dumps(invalid_data),
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if not result.get('success'):
                print("✅ Correctly handled invalid SPO code")
            else:
                print("❌ Should have failed for invalid SPO code")
        else:
            print(f"⚠️ Invalid SPO test returned status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing invalid SPO: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 TESTING COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_email_sending() 