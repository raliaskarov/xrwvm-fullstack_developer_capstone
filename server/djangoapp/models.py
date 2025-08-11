# server/djangoapp/models.py

from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# car make model
class CarMake(models.Model):

    MAKER_CHOICES = [
        (CHRYSLER: 'Chrysler'),
        (MERCEDES: 'MERCEDES'),
        (FORD: 'FORD'),
        (VOLVO: 'Volvo'),
        (GEELY: 'Geely')
        ]

    maker_name = models.CharField(null=False,
                    max_length=200,
                    default='not_selected',
                    choices=MAKER_CHOICES)

    description = models.CharField(null=True, max_length=200)

    def __str__(self):
        return self.
# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
