# Generated manually on 2025-08-18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0048_add_gst_status_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cfaagreement',
            name='gst_no',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
