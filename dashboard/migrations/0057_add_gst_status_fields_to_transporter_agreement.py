# Generated manually to add GST status fields to TransporterAgreement

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0056_add_type_of_approval_to_transporter_agreement'),
    ]

    operations = [
        # Add GST Status fields
        migrations.AddField(
            model_name='transporteragreement',
            name='gst_status',
            field=models.CharField(
                max_length=3,
                choices=[
                    ('YES', 'YES'),
                    ('NO', 'NO'),
                ],
                verbose_name='GST Status',
                default='NO'
            ),
        ),
        migrations.AddField(
            model_name='transporteragreement',
            name='state_code',
            field=models.CharField(
                max_length=2,
                blank=True,
                null=True,
                verbose_name='State Code'
            ),
        ),
        migrations.AddField(
            model_name='transporteragreement',
            name='pan_number',
            field=models.CharField(
                max_length=10,
                blank=True,
                null=True,
                verbose_name='PAN Number'
            ),
        ),
        migrations.AddField(
            model_name='transporteragreement',
            name='entity_code',
            field=models.CharField(
                max_length=4,
                blank=True,
                null=True,
                verbose_name='Entity Code'
            ),
        ),
        migrations.AddField(
            model_name='transporteragreement',
            name='declaration_rcm',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('Declaration', 'Declaration'),
                    ('RCM', 'RCM'),
                ],
                blank=True,
                null=True,
                verbose_name='Declaration/RCM'
            ),
        ),
        migrations.AddField(
            model_name='transporteragreement',
            name='declaration_status',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('Collected', 'Collected'),
                    ('Pending', 'Pending'),
                ],
                blank=True,
                null=True,
                verbose_name='Declaration Status'
            ),
        ),
        # Make gst_no nullable
        migrations.AlterField(
            model_name='transporteragreement',
            name='gst_no',
            field=models.CharField(
                max_length=20,
                blank=True,
                null=True,
                verbose_name='GST Number'
            ),
        ),
    ]
