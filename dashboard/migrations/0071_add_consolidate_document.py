# Generated manually to add consolidate_document field
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0070_update_file_size_to_50mb'),
    ]

    operations = [
        migrations.AddField(
            model_name='sporent',
            name='consolidate_document',
            field=models.FileField(blank=True, help_text='Consolidate Document (Max file size: 50 MB)', null=True, upload_to='spo_rent_attachments/', verbose_name='Consolidate Document'),
        ),
    ]
