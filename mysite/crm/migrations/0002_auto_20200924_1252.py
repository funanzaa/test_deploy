# Generated by Django 2.2.16 on 2020-09-24 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='case_pic',
            field=models.ImageField(blank=True, upload_to='cases/%Y/%m/%d'),
        ),
    ]