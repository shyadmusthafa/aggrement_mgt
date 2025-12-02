#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from dashboard.models import CFAAgreement, MasState

def test_cfa_model():
    print("Testing CFA Model Access...")
    
    try:
        # Check if we can count records
        total_count = CFAAgreement.objects.count()
        print(f"✓ Total CFA records: {total_count}")
        
        if total_count > 0:
            # Get a sample record
            sample = CFAAgreement.objects.first()
            print(f"✓ Sample record ID: {sample.id}")
            print(f"✓ Sample CFA code: {sample.cfa_code}")
            print(f"✓ Sample CFA name: {sample.cfa_name}")
            print(f"✓ Sample branch name: {sample.branch_name}")
            print(f"✓ Sample owner name: {sample.owner_name}")
            print(f"✓ Sample status: {sample.status}")
            
            # Check if state relationship works
            if sample.state:
                print(f"✓ Sample state: {sample.state.state_name}")
            else:
                print("✗ Sample state: None")
                
        else:
            print("⚠ No CFA records found in database")
            
        # Check if we can access related models
        state_count = MasState.objects.count()
        print(f"✓ Total states: {state_count}")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cfa_model()
