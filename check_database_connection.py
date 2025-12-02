#!/usr/bin/env python
"""
Script to check database connection and verify data_management database
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
from django.core.management import execute_from_command_line

def check_database_connection():
    """Check if we can connect to the data_management database"""
    print("=== Database Connection Check ===\n")
    
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ Successfully connected to MySQL")
            print(f"📊 MySQL Version: {version[0]}")
            
            # Check if data_management database exists
            cursor.execute("SHOW DATABASES LIKE 'data_management'")
            db_exists = cursor.fetchone()
            
            if db_exists:
                print(f"✅ Database 'data_management' exists")
                
                # Use the database
                cursor.execute("USE data_management")
                print(f"✅ Using database 'data_management'")
                
                # Check existing tables
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"\n📋 Existing tables in data_management:")
                for table in tables:
                    print(f"   - {table[0]}")
                
                # Check mas_construction table specifically
                cursor.execute("SHOW TABLES LIKE 'mas_construction'")
                construction_table = cursor.fetchone()
                if construction_table:
                    print(f"\n✅ mas_construction table exists")
                    
                    # Check table structure
                    cursor.execute("DESCRIBE mas_construction")
                    columns = cursor.fetchall()
                    print(f"\n📊 mas_construction table structure:")
                    for col in columns:
                        print(f"   - {col[0]}: {col[1]} ({col[2]})")
                    
                    # Check data count
                    cursor.execute("SELECT COUNT(*) FROM mas_construction")
                    count = cursor.fetchone()[0]
                    print(f"\n📈 Records in mas_construction: {count}")
                    
                    if count > 0:
                        # Show sample data
                        cursor.execute("SELECT * FROM mas_construction LIMIT 5")
                        sample_data = cursor.fetchall()
                        print(f"\n📝 Sample data:")
                        for row in sample_data:
                            print(f"   ID: {row[0]}, Name: {row[1]}, Remark: {row[2]}, Status: {row[3]}")
                else:
                    print(f"\n❌ mas_construction table does not exist")
                
            else:
                print(f"❌ Database 'data_management' does not exist")
                print(f"💡 You need to create the database first:")
                print(f"   CREATE DATABASE data_management;")
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print(f"\n🔧 Troubleshooting steps:")
        print(f"   1. Make sure MySQL server is running")
        print(f"   2. Check MySQL credentials in settings.py")
        print(f"   3. Create data_management database if it doesn't exist")
        print(f"   4. Ensure MySQL user has proper permissions")

def run_migrations():
    """Run Django migrations"""
    print(f"\n=== Running Django Migrations ===\n")
    
    try:
        # Run migrations
        execute_from_command_line(['manage.py', 'migrate'])
        print(f"✅ Migrations completed successfully")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == '__main__':
    check_database_connection()
    run_migrations() 