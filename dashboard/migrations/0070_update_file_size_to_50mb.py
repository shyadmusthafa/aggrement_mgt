# Generated manually to update file size help text to 50MB
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0069_update_entity_code_max_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sporent',
            name='transporter_agreement',
            field=models.FileField(blank=True, help_text='Rent Agreement (Max file size: 50 MB)', null=True, upload_to='spo_rent_attachments/', verbose_name='Rent Agreement'),
        ),
        migrations.AlterField(
            model_name='sporent',
            name='closure_letter',
            field=models.FileField(blank=True, help_text='Closure Letter (Max file size: 50 MB)', null=True, upload_to='spo_rent_attachments/'),
        ),
        migrations.AlterField(
            model_name='sporent',
            name='closure_acceptance_letter',
            field=models.FileField(blank=True, help_text='Closure Acceptance Letter (Max file size: 50 MB)', null=True, upload_to='spo_rent_attachments/'),
        ),
        migrations.AlterField(
            model_name='sporent',
            name='ff_letter_calc',
            field=models.FileField(blank=True, help_text='F&F Letter & Calc. (Max file size: 50 MB)', null=True, upload_to='spo_rent_attachments/'),
        ),
        migrations.AlterField(
            model_name='sporent',
            name='security_deposit',
            field=models.FileField(blank=True, help_text='Security Deposit (Max file size: 50 MB)', null=True, upload_to='spo_rent_attachments/'),
        ),
        migrations.AlterField(
            model_name='sporent',
            name='kyc_document',
            field=models.FileField(blank=True, help_text='KYC Document (Max file size: 50 MB)', null=True, upload_to='spo_rent_attachments/', verbose_name='KYC Document'),
        ),
        migrations.AlterField(
            model_name='sporent',
            name='bank_details',
            field=models.FileField(blank=True, help_text='Bank Details Document (Max file size: 50 MB)', null=True, upload_to='spo_rent_attachments/', verbose_name='Bank Details'),
        ),
    ]
