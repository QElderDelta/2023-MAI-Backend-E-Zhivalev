from django.core.validators import MinValueValidator
from django.db import models


class EngineType(models.Model):
    name = models.CharField(max_length=50, blank=False)


class CarBrand(models.Model):
    name = models.CharField(max_length=50, blank=False)


class CarModel(models.Model):
    name = models.CharField(max_length=50, blank=False)
    brand_id = models.OneToOneField(CarBrand, on_delete=models.CASCADE)


class Listing(models.Model):
    car_brand = models.OneToOneField(CarBrand, on_delete=models.CASCADE)
    car_model = models.OneToOneField(CarModel, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(1)])
    mileage = models.PositiveIntegerField()
    number_of_owners = models.PositiveIntegerField(
        validators=[MinValueValidator(0)])
    engine_type = models.OneToOneField(EngineType, on_delete=models.CASCADE)
    engine_volume = models.FloatField(validators=[MinValueValidator(0.01)])
    horse_power = models.PositiveIntegerField(
        validators=[MinValueValidator(1)])
