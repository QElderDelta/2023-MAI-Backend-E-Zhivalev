# Generated by Django 4.1.7 on 2023-05-29 14:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('brand_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.carbrand')),
            ],
        ),
        migrations.CreateModel(
            name='EngineType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('mileage', models.PositiveIntegerField()),
                ('number_of_owners', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('engine_volume', models.FloatField(validators=[django.core.validators.MinValueValidator(0.01)])),
                ('horse_power', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('car_brand', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.carbrand')),
                ('car_model', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.carmodel')),
                ('engine_type', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='listings.enginetype')),
            ],
        ),
    ]