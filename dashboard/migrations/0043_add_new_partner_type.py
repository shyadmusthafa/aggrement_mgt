# Generated manually to fix database schema mismatch - add new_partner_type field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0042_alter_masdistrict_options'),
    ]

    operations = [
        # Add only the missing new_partner_type field
        migrations.AddField(
            model_name='sporent',
            name='new_partner_type',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='New Partner Type'),
        ),
    ]
