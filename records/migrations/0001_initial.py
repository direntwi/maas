# Generated by Django 4.2.1 on 2023-08-29 14:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('drivers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Records',
            fields=[
                ('timestamp', models.DateTimeField(auto_now=True, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=20)),
                ('start_latitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('start_longitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('end_latitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('end_longitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('commuter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drivers.vehicle')),
            ],
        ),
    ]