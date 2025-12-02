# Generated manually to remove age field from MasPartnerDetails

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0061_remove_age_from_cfa_partner_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maspartnerdetails',
            name='age',
        ),
    ]
