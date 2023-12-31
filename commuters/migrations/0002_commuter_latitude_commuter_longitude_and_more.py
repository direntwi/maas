# Generated by Django 4.2.1 on 2023-08-29 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commuters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commuter',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='commuter',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='commuter',
            name='password',
            field=models.CharField(max_length=50),
        ),
    ]
