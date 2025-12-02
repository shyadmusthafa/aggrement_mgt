#!/usr/bin/env python
"""
Python script to connect to MySQL database data_management 
and insert data into mas_construction table
"""
import mysql.connector
from mysql.connector import Error

def connect_to_mysql():
    """Connect to MySQL database data_management"""
    try:
        # MySQL connection configuration
        connection = mysql.connector.connect(
            host='localhost',          # Change if your MySQL is on different host
            database='data_management', # Your database name
            user='root',               # Change to your MySQL username
            password='',               # Change to your MySQL password
            port=3306                  # Change if using different port
        )
        
        if connection.is_connected():
            print("✅ Successfully connected to MySQL database 'data_management'")
            return connection
        else:
            print("❌ Failed to connect to MySQL database")
            return None
            
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

def create_mas_construction_table(connection):
    """Create mas_construction table if it doesn't exist"""
    try:
        cursor = connection.cursor()
        
        # Create table SQL
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
        print("✅ mas_construction table created/verified successfully")
        
    except Error as e:
        print(f"❌ Error creating table: {e}")

def insert_construction_data(connection, construction_data):
    """Insert construction data into mas_construction table"""
    try:
        cursor = connection.cursor()
        
        # Check current data count
        cursor.execute("SELECT COUNT(*) FROM mas_construction")
        current_count = cursor.fetchone()[0]
        print(f"📊 Current records in table: {current_count}")
        
        # Insert data
        inserted_count = 0
        skipped_count = 0
        
        for name, remark, status in construction_data:
            try:
                # Check if record already exists
                cursor.execute("SELECT id FROM mas_construction WHERE name = %s", (name,))
                if cursor.fetchone():
                    print(f"⏭️  {name} - Already exists (skipped)")
                    skipped_count += 1
                else:
                    # Insert new record
                    insert_query = """
                    INSERT INTO mas_construction (name, remark, status) 
                    VALUES (%s, %s, %s)
                    """
                    cursor.execute(insert_query, (name, remark, status))
                    print(f"✅ {name} - Inserted successfully")
                    inserted_count += 1
                    
            except Error as e:
                print(f"❌ {name} - Error: {e}")
        
        # Commit the changes
        connection.commit()
        
        # Final verification
        cursor.execute("SELECT COUNT(*) FROM mas_construction")
        final_count = cursor.fetchone()[0]
        
        print(f"\n📈 Insertion Summary:")
        print(f"   - Records inserted: {inserted_count}")
        print(f"   - Records skipped: {skipped_count}")
        print(f"   - Total records now: {final_count}")
        
        return True
        
    except Error as e:
        print(f"❌ Error inserting data: {e}")
        return False

def display_all_data(connection):
    """Display all data from mas_construction table"""
    try:
        cursor = connection.cursor()
        
        # Get all data
        cursor.execute("SELECT * FROM mas_construction ORDER BY name")
        rows = cursor.fetchall()
        
        print(f"\n🏗️ All Construction Types in Database:")
        print("-" * 70)
        for row in rows:
            status_text = "✅ Active" if row[3] == 1 else "❌ Inactive"
            print(f"ID: {row[0]:2d} | {row[1]}")
            print(f"     Remark: {row[2]}")
            print(f"     Status: {status_text}")
            print()
            
    except Error as e:
        print(f"❌ Error displaying data: {e}")

def main():
    """Main function to connect and insert data"""
    
    print("=== MySQL Construction Data Insertion ===\n")
    
    # Step 1: Connect to MySQL
    connection = connect_to_mysql()
    if not connection:
        return
    
    try:
        # Step 2: Create table if not exists
        create_mas_construction_table(connection)
        
        # Step 3: Prepare construction data (you can modify this data)
        construction_data = [
            ('RCC Roof (Reinforced Cement Concrete)', 'Reinforced Cement Concrete roof structure', 1),
            ('Tin Sheet Roof', 'Tin sheet roofing material', 1),
            ('Container Structure', 'Container-based construction', 1),
            ('UPVC Sheet Roof', 'Unplasticized Polyvinyl Chloride sheet roofing', 1),
            ('Asbestos Sheet Roof', 'Asbestos sheet roofing material', 1),
            ('Concrete Roof', 'Concrete roof structure', 1),
            ('Thatched Roof', 'Thatched roof construction', 1),
            ('GI Sheet Roof (Galvanized Iron)', 'Galvanized Iron sheet roofing', 1),
            ('Metal Sheet Roof', 'Metal sheet roofing material', 1),
            ('Polycarbonate Sheet Roof', 'Polycarbonate sheet roofing', 1),
            ('Wooden Structure', 'Wooden construction structure', 1),
            ('Brick Masonry Building', 'Brick masonry construction', 1),
            ('Pre-fabricated Structure', 'Pre-fabricated building structure', 1),
            ('Fiber Sheet Roof', 'Fiber sheet roofing material', 1),
            ('Tiled Roof', 'Tiled roof construction', 1)
        ]
        
        # Step 4: Insert data
        print(f"\n📝 Inserting {len(construction_data)} construction types...")
        success = insert_construction_data(connection, construction_data)
        
        if success:
            # Step 5: Display all data
            display_all_data(connection)
            print("🎉 Data insertion completed successfully!")
        else:
            print("❌ Data insertion failed!")
            
    except Error as e:
        print(f"❌ Error: {e}")
        
    finally:
        # Close connection
        if connection.is_connected():
            connection.close()
            print("🔌 MySQL connection closed")

if __name__ == '__main__':
    main() 