# Generated manually to add consolidate_attachment field to CFAAgreement

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0071_add_consolidate_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfaagreement',
            name='consolidate_attachment',
            field=models.FileField(blank=True, help_text='Consolidate Attachment (Max file size: 50 MB)', null=True, upload_to='cfa_agreements/', verbose_name='Consolidate Attachment'),
        ),
    ]
