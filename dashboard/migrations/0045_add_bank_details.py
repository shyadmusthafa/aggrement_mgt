# Generated manually: add missing bank_details field to SPORent

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0044_add_kyc_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='sporent',
            name='bank_details',
            field=models.FileField(
                upload_to='spo_rent_attachments/',
                verbose_name='Bank Details',
                help_text='Bank Details Document (Max file size: 10 MB)',
                null=True,
                blank=True,
            ),
        ),
    ]
