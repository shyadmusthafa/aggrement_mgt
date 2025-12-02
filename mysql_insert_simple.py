#!/usr/bin/env python
"""
Simple Python script to connect to MySQL database data_management 
and insert data into mas_construction table
"""
import mysql.connector
from mysql.connector import Error

# ========================================
# CONFIGURATION - MODIFY THESE SETTINGS
# ========================================
MYSQL_CONFIG = {
    'host': '172.27.1.74',           # Change if your MySQL is on different host
    'database': 'data_management', # Your database name
    'user': 'raam',                # Change to your MySQL username
    'password': 'raam',                # Change to your MySQL password
    'port': 3306                   # Change if using different port
}

# ========================================
# CONSTRUCTION DATA - NAMES GO TO REMARKS COLUMN
# ========================================
CONSTRUCTION_DATA = [
    # Format: ('Name', 'Remark', Status)
    # Name: Will be inserted into name column
    # Remark: Will be inserted into remarks column  
    # Status: Will be set to 1
    ('RCC Roof', 'RCC Roof (Reinforced Cement Concrete)', 1),
    ('Tin Sheet Roof', 'Tin Sheet Roof', 1),
    ('Container Structure', 'Container Structure', 1),
    ('UPVC Sheet Roof', 'UPVC Sheet Roof', 1),
    ('Asbestos Sheet Roof', 'Asbestos Sheet Roof', 1),
    ('Concrete Roof', 'Concrete Roof', 1),
    ('Thatched Roof', 'Thatched Roof', 1),
    ('GI Sheet Roof', 'GI Sheet Roof (Galvanized Iron)', 1),
    ('Metal Sheet Roof', 'Metal Sheet Roof', 1),
    ('Polycarbonate Sheet Roof', 'Polycarbonate Sheet Roof', 1),
    ('Wooden Structure', 'Wooden Structure', 1),
    ('Brick Masonry Building', 'Brick Masonry Building', 1),
    ('Pre-fabricated Structure', 'Pre-fabricated Structure', 1),
    ('Fiber Sheet Roof', 'Fiber Sheet Roof', 1),
    ('Tiled Roof', 'Tiled Roof', 1),
    # Add more construction types here...
]

def main():
    """Main function to connect and insert data"""
    
    print("=== MySQL Construction Data Insertion ===\n")
    
    try:
        # Connect to MySQL
        print("🔌 Connecting to MySQL database...")
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        
        if connection.is_connected():
            print("✅ Successfully connected to MySQL database 'data_management'")
            
            cursor = connection.cursor()
            
            # Create table if not exists
            print("\n📋 Creating/verifying mas_construction table...")
            create_table_query = """
            CREATE TABLE IF NOT EXISTS mas_construction (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(200) UNIQUE NOT NULL,
                remark TEXT,
                status INT NOT NULL DEFAULT 1
            );
            """
            cursor.execute(create_table_query)
            connection.commit()
            print("✅ Table ready!")
            
            # Check current data
            cursor.execute("SELECT COUNT(*) FROM mas_construction")
            current_count = cursor.fetchone()[0]
            print(f"📊 Current records: {current_count}")
            
            # Insert data
            print(f"\n📝 Inserting {len(CONSTRUCTION_DATA)} construction types...")
            print("📋 Format: Name -> name column, Full name -> remarks column, Status = 1")
            inserted = 0
            skipped = 0
            
            for name, remark, status in CONSTRUCTION_DATA:
                try:
                    # Check if exists
                    cursor.execute("SELECT id FROM mas_construction WHERE name = %s", (name,))
                    if cursor.fetchone():
                        print(f"⏭️  {name} - Already exists")
                        skipped += 1
                    else:
                        # Insert new record
                        cursor.execute("""
                            INSERT INTO mas_construction (name, remark, status) 
                            VALUES (%s, %s, %s)
                        """, (name, remark, status))
                        print(f"✅ {name} - Inserted (Remark: {remark}, Status: {status})")
                        inserted += 1
                        
                except Error as e:
                    print(f"❌ {name} - Error: {e}")
            
            # Commit changes
            connection.commit()
            
            # Final count
            cursor.execute("SELECT COUNT(*) FROM mas_construction")
            final_count = cursor.fetchone()[0]
            
            print(f"\n📈 Summary:")
            print(f"   - Inserted: {inserted}")
            print(f"   - Skipped: {skipped}")
            print(f"   - Total: {final_count}")
            
            # Show all data
            print(f"\n🏗️ All Construction Types:")
            print("-" * 70)
            cursor.execute("SELECT * FROM mas_construction ORDER BY name")
            for row in cursor.fetchall():
                status = "Active" if row[3] == 1 else "Inactive"
                print(f"ID: {row[0]:2d} | Name: {row[1]}")
                print(f"     Remark: {row[2]}")
                print(f"     Status: {status}")
                print()
            
            print("\n🎉 Data insertion completed!")
            
        else:
            print("❌ Failed to connect to MySQL")
            
    except Error as e:
        print(f"❌ Error: {e}")
        
    finally:
        # Close connection
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("🔌 MySQL connection closed")

if __name__ == '__main__':
    main() 