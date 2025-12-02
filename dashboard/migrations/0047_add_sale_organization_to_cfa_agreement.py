# Generated manually to add sale_organization field to CFAAgreement

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0046_fix_declaration_status_column'),
    ]

    operations = [
        migrations.RunSQL(
            # Forward SQL: Add sale_organization column
            sql="""
            ALTER TABLE dashboard_cfaagreement 
            ADD COLUMN sale_organization VARCHAR(50) NULL;
            """,
            # Reverse SQL: Remove the column if needed
            reverse_sql="""
            ALTER TABLE dashboard_cfaagreement 
            DROP COLUMN sale_organization;
            """
        ),
    ]
