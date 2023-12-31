# Generated by Django 4.2.1 on 2023-08-29 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('registration_number', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=20)),
                ('make', models.CharField(max_length=20)),
                ('colour', models.CharField(max_length=20)),
                ('seats', models.IntegerField()),
                ('available_seats', models.IntegerField()),
                ('driver', models.ManyToManyField(to='drivers.driver')),
            ],
        ),
    ]
