# Generated by Django 2.2.16 on 2020-12-17 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_auto_20201217_1609'),
    ]

    operations = [
        migrations.RenameField(
            model_name='model5_recap_report',
            old_name='err_cod',
            new_name='err_code',
        ),
    ]