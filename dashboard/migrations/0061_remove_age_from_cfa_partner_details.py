# Generated manually to remove age field from CFAPartnerDetails

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0060_fix_transporter_partner_validation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cfapartnerdetails',
            name='age',
        ),
    ]
