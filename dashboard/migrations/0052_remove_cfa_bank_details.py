# Generated manually on 2025-08-18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0051_add_cfa_kyc_bank_attachments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cfaagreement',
            name='bank_details',
        ),
    ]
