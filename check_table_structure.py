#!/usr/bin/env python
"""
Script to check the structure of mas_construction table
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

def check_table_structure():
    """Check the structure of mas_construction table"""
    
    print("🔍 Checking mas_construction table structure...")
    
    try:
        with connection.cursor() as cursor:
            # Check if table exists
            cursor.execute("SHOW TABLES LIKE 'mas_construction'")
            table_exists = cursor.fetchone()
            
            if not table_exists:
                print("❌ mas_construction table does not exist!")
                return
            
            print("✅ mas_construction table exists")
            
            # Get table structure
            cursor.execute("DESCRIBE mas_construction")
            columns = cursor.fetchall()
            
            print(f"\n📊 Table structure:")
            print(f"{'Field':<20} {'Type':<20} {'Null':<10} {'Key':<10} {'Default':<10} {'Extra':<10}")
            print("-" * 80)
            
            for col in columns:
                print(f"{col[0]:<20} {col[1]:<20} {col[2]:<10} {col[3]:<10} {str(col[4]):<10} {col[5]:<10}")
            
            # Check existing data
            cursor.execute("SELECT COUNT(*) FROM mas_construction")
            count = cursor.fetchone()[0]
            print(f"\n📈 Total records: {count}")
            
            if count > 0:
                cursor.execute("SELECT * FROM mas_construction LIMIT 5")
                records = cursor.fetchall()
                print(f"\n📝 Sample data:")
                for record in records:
                    print(f"   {record}")
                    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_table_structure() 