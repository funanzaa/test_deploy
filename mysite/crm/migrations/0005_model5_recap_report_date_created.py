# Generated by Django 2.2.16 on 2020-12-17 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_model5_recap_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='model5_recap_report',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
