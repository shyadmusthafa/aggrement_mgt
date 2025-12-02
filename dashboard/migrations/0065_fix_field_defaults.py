# Generated manually to fix field defaults in UserMenuAccess

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0064_add_legacy_fields_to_usermenuaccess'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermenuaccess',
            name='can_view',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='usermenuaccess',
            name='can_create',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='usermenuaccess',
            name='can_edit',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='usermenuaccess',
            name='can_delete',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='usermenuaccess',
            name='can_approve',
            field=models.BooleanField(default=True),
        ),
    ]
