# Generated manually to remove age field from TransporterPartnerDetails

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0058_add_kyc_document_to_transporter_agreement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transporterpartnerdetails',
            name='age',
        ),
    ]
