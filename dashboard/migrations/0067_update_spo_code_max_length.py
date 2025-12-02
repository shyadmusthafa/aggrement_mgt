# Generated manually to update SPO Code field maximum length

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0066_force_recreate_usermenuaccess_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sporent',
            name='spo_code',
            field=models.CharField(help_text='Maximum 4 characters', max_length=4, unique=True, verbose_name='SPO Code'),
        ),
    ]
