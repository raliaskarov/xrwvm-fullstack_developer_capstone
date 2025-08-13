from django.contrib import admin
from .models import CarMake, CarModel


# Register models

admin.site.register(CarMake)
admin.site.register(CarModel)
