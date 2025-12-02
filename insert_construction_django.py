#!/usr/bin/env python
"""
Django script to insert construction data into mas_construction table using ORM
"""
import os
import django
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from dashboard.models import MasConstruction

def insert_construction_data_django():
    """Insert construction data using Django ORM"""
    
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
    
    print("🏗️  Construction Data Insertion Script (Django ORM)")
    print("=" * 60)
    
    try:
        # Check if MasConstruction model exists
        print("🔍 Checking MasConstruction model...")
        
        # Get existing records count
        existing_count = MasConstruction.objects.count()
        print(f"📊 Existing records in mas_construction: {existing_count}")
        
        # Insert data
        print(f"\n📝 Inserting {len(construction_data)} construction types...")
        
        inserted_count = 0
        skipped_count = 0
        
        for construction_name in construction_data:
            try:
                # Check if record already exists
                existing = MasConstruction.objects.filter(name=construction_name).first()
                
                if existing:
                    print(f"   ⚠️  Skipped (already exists): {construction_name}")
                    skipped_count += 1
                else:
                    # Create new record
                    MasConstruction.objects.create(
                        name=construction_name,
                        remark='',  # Empty remark
                        status=1    # Active status
                    )
                    inserted_count += 1
                    print(f"   ✅ Inserted: {construction_name}")
                    
            except Exception as e:
                print(f"   ❌ Error inserting {construction_name}: {e}")
        
        print(f"\n📊 Insertion Summary:")
        print(f"   ✅ Successfully inserted: {inserted_count}")
        print(f"   ⚠️  Skipped (duplicates): {skipped_count}")
        print(f"   📈 Total processed: {len(construction_data)}")
        
        # Verify the data
        print(f"\n🔍 Verifying data in mas_construction table...")
        total_count = MasConstruction.objects.count()
        print(f"   📊 Total records in table: {total_count}")
        
        # Show all records
        print(f"\n📋 All records in mas_construction table:")
        print(f"{'ID':<5} {'Name':<40} {'Remark':<10} {'Status':<8}")
        print("-" * 70)
        
        records = MasConstruction.objects.all().order_by('id')
        for record in records:
            print(f"{record.id:<5} {record.name:<40} {record.remark or '':<10} {record.status:<8}")
        
        print(f"\n✅ Data insertion completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"\n🔧 Troubleshooting:")
        print(f"   1. Make sure MySQL server is running")
        print(f"   2. Check if data_management database exists")
        print(f"   3. Run Django migrations if needed:")
        print(f"      python manage.py makemigrations")
        print(f"      python manage.py migrate")

if __name__ == "__main__":
    insert_construction_data_django() 