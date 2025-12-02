#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection

def check_table_schema():
    """Check the current database schema for CFA and Transporter agreement tables"""
    
    with connection.cursor() as cursor:
        # Check CFA Agreement table
        print("=== CFA Agreement Table Schema ===")
        cursor.execute("DESCRIBE dashboard_cfaagreement")
        columns = cursor.fetchall()
        for column in columns:
            print(f"  {column[0]} - {column[1]} - {column[2]} - {column[3]} - {column[4]} - {column[5]}")
        
        print("\n=== Transporter Agreement Table Schema ===")
        cursor.execute("DESCRIBE dashboard_transporteragreement")
        columns = cursor.fetchall()
        for column in columns:
            print(f"  {column[0]} - {column[1]} - {column[2]} - {column[3]} - {column[4]} - {column[5]}")
        
        print("\n=== Checking for existing data ===")
        cursor.execute("SELECT COUNT(*) FROM dashboard_cfaagreement")
        cfa_count = cursor.fetchone()[0]
        print(f"CFA Agreement records: {cfa_count}")
        
        cursor.execute("SELECT COUNT(*) FROM dashboard_transporteragreement")
        transporter_count = cursor.fetchone()[0]
        print(f"Transporter Agreement records: {transporter_count}")

if __name__ == "__main__":
    check_table_schema()
