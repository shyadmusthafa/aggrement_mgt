# Generated manually to add list_of_plant field back to TransporterAgreement

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0053_transporter_agreement_sale_organization'),
    ]

    operations = [
        # Add list_of_plant field back
        migrations.AddField(
            model_name='transporteragreement',
            name='list_of_plant',
            field=models.TextField(blank=True),
        ),
    ]
