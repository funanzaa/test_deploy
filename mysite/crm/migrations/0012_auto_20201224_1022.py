# Generated by Django 2.2.16 on 2020-12-24 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_auto_20201219_1905'),
    ]

    operations = [
        migrations.RenameField(
            model_name='model5_recap_report',
            old_name='err_code',
            new_name='dataknow',
        ),
    ]
