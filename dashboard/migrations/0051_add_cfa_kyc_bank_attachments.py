# Generated manually on 2025-08-18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0050_remove_status_add_customer_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfaagreement',
            name='kyc_document',
            field=models.FileField(blank=True, null=True, upload_to='cfa_agreements/', verbose_name='KYC Document'),
        ),
        migrations.AddField(
            model_name='cfaagreement',
            name='bank_details',
            field=models.FileField(blank=True, null=True, upload_to='cfa_agreements/', verbose_name='Bank Details'),
        ),
    ]
