#!/usr/bin/env python
"""
Script to insert construction data into mas_construction table (fixed for actual structure)
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

def insert_construction_data_fixed():
    """Insert construction data using direct SQL to match actual table structure"""
    
    # Construction data to insert
    construction_data = [
        "RCC Roof (Reinforced Cement Concrete)",
        "Tin Sheet Roof",
        "Container Structure",
        "UPVC Sheet Roof",
        "Asbestos Sheet Roof",
        "Concrete Roof",
        "Thatched Roof",
        "GI Sheet Roof (Galvanized Iron)",
        "Metal Sheet Roof",
        "Polycarbonate Sheet Roof",
        "Wooden Structure",
        "Brick Masonry Building",
        "Pre-fabricated Structure",
        "Fiber Sheet Roof",
        "Tiled Roof"
    ]
    
    print("🏗️  Construction Data Insertion Script (Fixed)")
    print("=" * 50)
    
    try:
        with connection.cursor() as cursor:
            # Check if table exists
            cursor.execute("SHOW TABLES LIKE 'mas_construction'")
            table_exists = cursor.fetchone()
            
            if not table_exists:
                print("❌ mas_construction table does not exist!")
                return
            
            print("✅ mas_construction table found")
            
            # Get existing records count
            cursor.execute("SELECT COUNT(*) FROM mas_construction")
            existing_count = cursor.fetchone()[0]
            print(f"📊 Existing records: {existing_count}")
            
            # Insert data
            print(f"\n📝 Inserting {len(construction_data)} construction types...")
            
            inserted_count = 0
            skipped_count = 0
            
            for construction_name in construction_data:
                try:
                    # Check if record already exists
                    cursor.execute("SELECT id FROM mas_construction WHERE name = %s", [construction_name])
                    existing = cursor.fetchone()
                    
                    if existing:
                        print(f"   ⚠️  Skipped (already exists): {construction_name}")
                        skipped_count += 1
                    else:
                        # Insert new record - using actual table structure
                        insert_query = """
                        INSERT INTO mas_construction (name, remarks) 
                        VALUES (%s, %s)
                        """
                        values = (construction_name, '')  # Empty remarks
                        
                        cursor.execute(insert_query, values)
                        inserted_count += 1
                        print(f"   ✅ Inserted: {construction_name}")
                        
                except Exception as e:
                    print(f"   ❌ Error inserting {construction_name}: {e}")
            
            # Commit the changes
            connection.commit()
            
            print(f"\n📊 Insertion Summary:")
            print(f"   ✅ Successfully inserted: {inserted_count}")
            print(f"   ⚠️  Skipped (duplicates): {skipped_count}")
            print(f"   📈 Total processed: {len(construction_data)}")
            
            # Verify the data
            print(f"\n🔍 Verifying data in mas_construction table...")
            cursor.execute("SELECT COUNT(*) FROM mas_construction")
            total_count = cursor.fetchone()[0]
            print(f"   📊 Total records in table: {total_count}")
            
            # Show all records
            cursor.execute("SELECT id, name, remarks FROM mas_construction ORDER BY id")
            records = cursor.fetchall()
            
            print(f"\n📋 All records in mas_construction table:")
            print(f"{'ID':<5} {'Name':<40} {'Remarks':<10}")
            print("-" * 60)
            for record in records:
                print(f"{record[0]:<5} {record[1]:<40} {record[2] or '':<10}")
            
            print(f"\n✅ Data insertion completed successfully!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"\n🔧 Troubleshooting:")
        print(f"   1. Make sure MySQL server is running")
        print(f"   2. Check if data_management database exists")
        print(f"   3. Verify table structure")

if __name__ == "__main__":
    insert_construction_data_fixed() 