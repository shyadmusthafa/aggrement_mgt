# Generated manually on 2025-08-18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0047_add_sale_organization_to_cfa_agreement'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfaagreement',
            name='gst_status',
            field=models.CharField(
                blank=True,
                choices=[('YES', 'YES'), ('NO', 'NO')],
                max_length=10,
                null=True,
                verbose_name='GST Status'
            ),
        ),
        migrations.AddField(
            model_name='cfaagreement',
            name='state_code',
            field=models.CharField(
                blank=True,
                max_length=2,
                null=True,
                verbose_name='State Code'
            ),
        ),
        migrations.AddField(
            model_name='cfaagreement',
            name='pan_number',
            field=models.CharField(
                blank=True,
                max_length=10,
                null=True,
                verbose_name='PAN Number'
            ),
        ),
        migrations.AddField(
            model_name='cfaagreement',
            name='entity_code',
            field=models.CharField(
                blank=True,
                max_length=4,
                null=True,
                verbose_name='Last 4 Characters'
            ),
        ),
        migrations.AddField(
            model_name='cfaagreement',
            name='declaration_rcm',
            field=models.CharField(
                blank=True,
                choices=[('Declaration', 'Declaration'), ('RCM', 'RCM')],
                max_length=20,
                null=True,
                verbose_name='Declaration / RCM'
            ),
        ),
        migrations.AddField(
            model_name='cfaagreement',
            name='declaration_status',
            field=models.CharField(
                blank=True,
                choices=[('Collected', 'Collected'), ('Pending', 'Pending')],
                max_length=10,
                null=True,
                verbose_name='Declaration Status'
            ),
        ),
    ]
