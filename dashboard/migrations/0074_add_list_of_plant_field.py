# Generated manually to add list_of_plant field as CharField

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0073_remove_type_of_approval_field'),
    ]

    operations = [
        # Add the new list_of_plant field as CharField
        migrations.AddField(
            model_name='transporteragreement',
            name='list_of_plant',
            field=models.CharField(
                blank=True,
                max_length=500,
                null=True,
                verbose_name='List of Plant',
                help_text='Select multiple plants separated by commas'
            ),
        ),
    ]
