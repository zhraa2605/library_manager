# Generated by Django 5.1.1 on 2025-01-02 10:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_api', '0002_alter_userprofile_options_remove_userprofile_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
