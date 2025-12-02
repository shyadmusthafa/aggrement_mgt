# Generated manually to update TransporterAgreement model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0052_remove_cfa_bank_details'),
    ]

    operations = [
        # Add sale_organization field
        migrations.AddField(
            model_name='transporteragreement',
            name='sale_organization',
            field=models.CharField(
                blank=True,
                choices=[('Chettinad', 'Chettinad'), ('Anjani', 'Anjani')],
                max_length=50,
                null=True,
                verbose_name='Sale Organization'
            ),
        ),
        # Remove branch field
        migrations.RemoveField(
            model_name='transporteragreement',
            name='branch',
        ),
        # Remove list_of_plant field
        migrations.RemoveField(
            model_name='transporteragreement',
            name='list_of_plant',
        ),
    ]
