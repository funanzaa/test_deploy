# Generated by Django 2.2.16 on 2021-01-15 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0016_profileserver'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileserver',
            name='FirstOperationSystem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='crm.OperationSystem'),
        ),
    ]
