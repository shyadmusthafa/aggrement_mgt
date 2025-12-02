# Generated manually to add new menu access fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0067_update_spo_code_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermenuaccess',
            name='approval_workflow_enabled',
            field=models.BooleanField(default=True, verbose_name='Approval Workflow Enabled'),
        ),
        migrations.AddField(
            model_name='usermenuaccess',
            name='report_enabled',
            field=models.BooleanField(default=True, verbose_name='Report Enabled'),
        ),
        migrations.AddField(
            model_name='usermenuaccess',
            name='mail_reminder_enabled',
            field=models.BooleanField(default=True, verbose_name='Mail Reminder Enabled'),
        ),
        migrations.AddField(
            model_name='usermenuaccess',
            name='user_management_enabled',
            field=models.BooleanField(default=True, verbose_name='User Management Enabled'),
        ),
        migrations.AddField(
            model_name='usermenuaccess',
            name='user_menu_access_control_enabled',
            field=models.BooleanField(default=True, verbose_name='User Menu Access Control Enabled'),
        ),
    ]
