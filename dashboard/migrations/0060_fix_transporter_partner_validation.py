# Generated manually to fix validation issue in TransporterPartnerDetails

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0059_remove_age_from_transporter_partner_details'),
    ]

    operations = [
        # This migration is to ensure the model validation is updated
        # The age field validation has been removed from the model's clean method
    ]
