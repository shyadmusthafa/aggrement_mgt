# Generated manually to fix declaration_status column constraints

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0045_add_bank_details'),
    ]

    operations = [
        migrations.RunSQL(
            # Forward SQL: Make declaration_status column nullable and adjust size
            sql="""
            ALTER TABLE dashboard_sporent 
            MODIFY COLUMN declaration_status VARCHAR(10) NULL;
            """,
            # Reverse SQL: Revert changes if needed
            reverse_sql="""
            ALTER TABLE dashboard_sporent 
            MODIFY COLUMN declaration_status VARCHAR(100) NOT NULL;
            """
        ),
    ]
