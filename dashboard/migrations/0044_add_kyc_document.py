# Generated manually: add missing kyc_document field to SPORent

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0043_add_new_partner_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='sporent',
            name='kyc_document',
            field=models.FileField(
                upload_to='spo_rent_attachments/',
                verbose_name='KYC Document',
                help_text='KYC Document (Max file size: 10 MB)',
                null=True,
                blank=True,
            ),
        ),
    ]
