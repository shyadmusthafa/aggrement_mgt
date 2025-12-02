#!/usr/bin/env python3
"""
Script to create the mas_partner_details table manually
"""

import os
import sys
import django

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection

def create_partner_table():
    """Create the mas_partner_details table manually"""
    
    with connection.cursor() as cursor:
        # Check if table exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE() 
            AND table_name = 'mas_partner_details'
        """)
        
        table_exists = cursor.fetchone()[0] > 0
        
        if table_exists:
            print("✅ Table 'mas_partner_details' already exists!")
            return True
        
        # Create the table without foreign keys first
        cursor.execute("""
            CREATE TABLE mas_partner_details (
                id INT AUTO_INCREMENT PRIMARY KEY,
                spo_id INT NOT NULL,
                name VARCHAR(200) NOT NULL,
                gender VARCHAR(10) NOT NULL,
                age INT NOT NULL,
                address LONGTEXT NOT NULL,
                mail_id VARCHAR(254) NOT NULL,
                aadhar_no VARCHAR(12) NOT NULL,
                pan_no VARCHAR(10) NOT NULL,
                partner_join_date DATE NOT NULL,
                partner_end_date DATE NULL,
                created_at DATETIME(6) NOT NULL,
                updated_at DATETIME(6) NOT NULL,
                created_by_id INT NULL,
                UNIQUE KEY unique_spo_aadhar (spo_id, aadhar_no)
            )
        """)
        
        # Add foreign keys separately
        try:
            cursor.execute("""
                ALTER TABLE mas_partner_details 
                ADD CONSTRAINT fk_partner_spo 
                FOREIGN KEY (spo_id) REFERENCES dashboard_sporent(id) ON DELETE CASCADE
            """)
        except Exception as e:
            print(f"⚠️ Warning: Could not add SPO foreign key: {e}")
        
        try:
            cursor.execute("""
                ALTER TABLE mas_partner_details 
                ADD CONSTRAINT fk_partner_user 
                FOREIGN KEY (created_by_id) REFERENCES auth_user(id) ON DELETE SET NULL
            """)
        except Exception as e:
            print(f"⚠️ Warning: Could not add user foreign key: {e}")
        
        print("✅ Table 'mas_partner_details' created successfully!")
        return True

if __name__ == '__main__':
    print("🔧 Creating mas_partner_details table...")
    success = create_partner_table()
    
    if success:
        print("🎉 Partner table setup completed!")
    else:
        print("❌ Failed to create partner table.") 