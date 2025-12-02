# Generated manually to add missing columns to UserMenuAccess table

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0062_remove_age_from_mas_partner_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermenuaccess',
            name='spo_menu_enabled',
            field=models.BooleanField(default=True, verbose_name='SPO Menu Enabled'),
        ),
        migrations.AddField(
            model_name='usermenuaccess',
            name='cfa_menu_enabled',
            field=models.BooleanField(default=True, verbose_name='CFA Menu Enabled'),
        ),
        migrations.AddField(
            model_name='usermenuaccess',
            name='transport_menu_enabled',
            field=models.BooleanField(default=True, verbose_name='Transport Menu Enabled'),
        ),
        migrations.AddField(
            model_name='usermenuaccess',
            name='approval_menu_enabled',
            field=models.BooleanField(default=True, verbose_name='Approval Menu Enabled'),
        ),
    ]
