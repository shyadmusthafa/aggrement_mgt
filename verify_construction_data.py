#!/usr/bin/env python
"""
Script to verify construction data in mas_construction table
"""
import os
import django
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection

def verify_construction_data():
    """Verify and display construction data"""
    
    print("🔍 Verifying Construction Data in mas_construction table")
    print("=" * 60)
    
    try:
        with connection.cursor() as cursor:
            # Get total count
            cursor.execute("SELECT COUNT(*) FROM mas_construction")
            total_count = cursor.fetchone()[0]
            print(f"📊 Total records: {total_count}")
            
            if total_count == 0:
                print("❌ No data found in mas_construction table")
                return
            
            # Get all records
            cursor.execute("SELECT id, name, remarks FROM mas_construction ORDER BY id")
            records = cursor.fetchall()
            
            print(f"\n📋 All Construction Types:")
            print(f"{'ID':<5} {'Construction Type':<50}")
            print("-" * 60)
            
            for record in records:
                record_id = record[0] if record[0] is not None else 'N/A'
                record_name = record[1] if record[1] is not None else 'N/A'
                print(f"{record_id:<5} {record_name:<50}")
            
            print(f"\n✅ Verification completed successfully!")
            print(f"🎉 All {total_count} construction types are now available in the database!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_construction_data() 