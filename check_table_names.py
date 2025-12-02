#!/usr/bin/env python3
"""
Script to check table names in the database
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

def check_tables():
    """Check table names in the database"""
    
    with connection.cursor() as cursor:
        # Get all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE()
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        
        print("📋 Tables in database:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Check for SPO related tables
        spo_tables = [t[0] for t in tables if 'spo' in t[0].lower()]
        print(f"\n🔍 SPO related tables: {spo_tables}")

if __name__ == '__main__':
    check_tables() 