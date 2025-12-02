# Generated manually to add pincode field to TransporterAgreement

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0054_add_list_of_plant_back'),
    ]

    operations = [
        # Add pincode field
        migrations.AddField(
            model_name='transporteragreement',
            name='pincode',
            field=models.CharField(
                max_length=10,
                verbose_name='PIN Code',
                default=''
            ),
        ),
    ]
