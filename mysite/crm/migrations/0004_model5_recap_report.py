# Generated by Django 2.2.16 on 2020-12-17 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20201217_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='model5_recap_report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hcode', models.CharField(max_length=255)),
                ('hname', models.CharField(max_length=255)),
                ('req_claimcode', models.CharField(max_length=255)),
                ('req_claim', models.CharField(max_length=255)),
                ('approved', models.CharField(max_length=255)),
                ('denined', models.CharField(max_length=255)),
                ('total', models.CharField(max_length=255)),
            ],
        ),
    ]