from django.contrib import admin
from .models import *


@admin.register(EngineType)
class EngineTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    pass


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    pass
# Register your models here.
