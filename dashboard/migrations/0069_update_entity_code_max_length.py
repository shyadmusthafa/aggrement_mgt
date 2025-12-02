# Generated manually to update entity_code field max_length from 4 to 5

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0068_add_new_menu_access_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sporent',
            name='entity_code',
            field=models.CharField(max_length=5, verbose_name="Last 5 Characters", null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='cfaagreement',
            name='entity_code',
            field=models.CharField(max_length=5, verbose_name="Last 5 Characters", null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='transporteragreement',
            name='entity_code',
            field=models.CharField(max_length=5, blank=True, null=True, verbose_name="Entity Code"),
        ),
    ]
