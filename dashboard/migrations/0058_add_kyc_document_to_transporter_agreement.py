# Generated manually to add kyc_document field to TransporterAgreement

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0057_add_gst_status_fields_to_transporter_agreement'),
    ]

    operations = [
        migrations.AddField(
            model_name='transporteragreement',
            name='kyc_document',
            field=models.FileField(blank=True, null=True, upload_to='transporter_agreements/', verbose_name='KYC Document'),
        ),
    ]
