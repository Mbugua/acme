# Generated by Django 2.2.7 on 2019-11-29 18:47

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_plate', models.CharField(max_length=50)),
                ('capacity', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BusOrganisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('logo', models.ImageField(blank=True, upload_to='logo-pic/')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_location', models.CharField(max_length=255)),
                ('destination_location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=15)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Bus')),
            ],
            options={
                'ordering': ['price'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=255)),
                ('ticket_number', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('transaction_code', models.CharField(max_length=255)),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Schedule')),
            ],
        ),
        migrations.AddField(
            model_name='bus',
            name='bus_organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.BusOrganisation'),
        ),
        migrations.AddField(
            model_name='bus',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Route'),
        ),
    ]
