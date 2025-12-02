# Generated manually on 2025-08-18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0049_update_gst_no_nullable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cfaagreement',
            name='status',
        ),
        migrations.AddField(
            model_name='cfaagreement',
            name='customer_code',
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name='Customer Code'
            ),
        ),
    ]
