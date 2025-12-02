# Generated manually to add type_of_approval field to TransporterAgreement

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0055_add_pincode_to_transporter_agreement'),
    ]

    operations = [
        # Add type_of_approval field
        migrations.AddField(
            model_name='transporteragreement',
            name='type_of_approval',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('NFA', 'NFA'),
                    ('RENT', 'RENT'),
                    ('INTERNAL', 'INTERNAL'),
                    ('DCWC', 'DCWC'),
                    ('RP/SHORTAGE', 'RP/SHORTAGE'),
                    ('OTHERS', 'OTHERS'),
                ],
                verbose_name='Type of Approval',
                default='NFA'
            ),
        ),
    ]
