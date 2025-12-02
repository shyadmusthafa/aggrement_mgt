# Generated manually to force recreate UserMenuAccess table with proper defaults

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0065_fix_field_defaults'),
    ]

    operations = [
        # First, delete the existing table
        migrations.DeleteModel(
            name='UserMenuAccess',
        ),
        
        # Then recreate it with proper structure
        migrations.CreateModel(
            name='UserMenuAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spo_menu_enabled', models.BooleanField(default=True, verbose_name='SPO Menu Enabled')),
                ('cfa_menu_enabled', models.BooleanField(default=True, verbose_name='CFA Menu Enabled')),
                ('transport_menu_enabled', models.BooleanField(default=True, verbose_name='Transport Menu Enabled')),
                ('approval_menu_enabled', models.BooleanField(default=True, verbose_name='Approval Menu Enabled')),
                ('can_view', models.BooleanField(default=True)),
                ('can_create', models.BooleanField(default=True)),
                ('can_edit', models.BooleanField(default=True)),
                ('can_delete', models.BooleanField(default=True)),
                ('can_approve', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='menu_access', to='auth.user')),
            ],
            options={
                'verbose_name': 'User Menu Access',
                'verbose_name_plural': 'User Menu Access',
            },
        ),
    ]
