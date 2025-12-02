#!/usr/bin/env python
"""
Script to insert construction data into mas_construction table
"""
import mysql.connector
from mysql.connector import Error

def insert_construction_data():
    """Insert construction data into mas_construction table"""
    
    # Database connection configuration
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'data_management',
        'charset': 'utf8mb4'
    }
    
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
    
    try:
        # Establish database connection
        print("🔌 Connecting to MySQL database...")
        connection = mysql.connector.connect(**db_config)
        
        if connection.is_connected():
            print("✅ Successfully connected to MySQL database")
            print(f"📊 Database: {db_config['database']}")
            
            # Create cursor
            cursor = connection.cursor()
            
            # Check if mas_construction table exists
            cursor.execute("SHOW TABLES LIKE 'mas_construction'")
            table_exists = cursor.fetchone()
            
            if not table_exists:
                print("❌ mas_construction table does not exist!")
                print("💡 Please run Django migrations first:")
                print("   python manage.py makemigrations")
                print("   python manage.py migrate")
                return
            
            print("✅ mas_construction table found")
            
            # Insert data
            print(f"\n📝 Inserting {len(construction_data)} construction types...")
            
            inserted_count = 0
            skipped_count = 0
            
            for construction_name in construction_data:
                try:
                    # Insert with default values for remark and status
                    insert_query = """
                    INSERT INTO mas_construction (name, remark, status) 
                    VALUES (%s, %s, %s)
                    """
                    values = (construction_name, '', 1)  # Empty remark, status = 1 (active)
                    
                    cursor.execute(insert_query, values)
                    inserted_count += 1
                    print(f"   ✅ Inserted: {construction_name}")
                    
                except mysql.connector.IntegrityError as e:
                    if "Duplicate entry" in str(e):
                        print(f"   ⚠️  Skipped (already exists): {construction_name}")
                        skipped_count += 1
                    else:
                        print(f"   ❌ Error inserting {construction_name}: {e}")
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
            cursor.execute("SELECT id, name, remark, status FROM mas_construction ORDER BY id")
            records = cursor.fetchall()
            
            print(f"\n📋 All records in mas_construction table:")
            print(f"{'ID':<5} {'Name':<40} {'Remark':<10} {'Status':<8}")
            print("-" * 70)
            for record in records:
                print(f"{record[0]:<5} {record[1]:<40} {record[2]:<10} {record[3]:<8}")
            
    except Error as e:
        print(f"❌ Database connection error: {e}")
        print(f"\n🔧 Troubleshooting:")
        print(f"   1. Make sure MySQL server is running")
        print(f"   2. Check if data_management database exists")
        print(f"   3. Verify MySQL credentials")
        print(f"   4. Ensure mas_construction table exists")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        
    finally:
        # Close database connection
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print(f"\n🔌 Database connection closed")

if __name__ == "__main__":
    print("🏗️  Construction Data Insertion Script")
    print("=" * 50)
    insert_construction_data() 