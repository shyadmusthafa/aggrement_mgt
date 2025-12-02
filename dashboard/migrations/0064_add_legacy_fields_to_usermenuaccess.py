# Generated manually to add legacy fields to UserMenuAccess

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0063_add_missing_columns_to_usermenuaccess'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermenuaccess',
            name='can_view',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usermenuaccess',
            name='can_create',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usermenuaccess',
            name='can_edit',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usermenuaccess',
            name='can_delete',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usermenuaccess',
            name='can_approve',
            field=models.BooleanField(default=True),
        ),
    ]
