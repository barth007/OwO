# Generated by Django 4.2.9 on 2024-01-11 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_account_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kyc',
            name='account',
        ),
    ]
