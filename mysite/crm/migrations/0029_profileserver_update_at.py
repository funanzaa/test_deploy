# Generated by Django 2.2.16 on 2021-01-15 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0028_auto_20210115_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileserver',
            name='update_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
