# Generated by Django 2.2.16 on 2020-12-17 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20201217_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model5_lookup_error',
            name='err_code',
            field=models.TextField(),
        ),
    ]
