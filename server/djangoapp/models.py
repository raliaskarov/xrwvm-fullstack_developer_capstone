# server/djangoapp/models.py

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# car make model
class CarMake(models.Model):

    MAKER_CHOICES = [
        ('NOT_SELECTED', 'Not Selected'),
        ('CHRYSLER', 'Chrysler'),
        ('MERCEDES', 'MERCEDES'),
        ('FORD', 'FORD'),
        ('VOLVO', 'Volvo'),
        ('GEELY', 'Geely')
        ]

    name = models.CharField(
        null=False,
        max_length=200,
        default='NOT_SELECTED',
        choices=MAKER_CHOICES
    )

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# car model model
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name= models.CharField(max_length=100)
    MODEL_CHOICES = [
        ('NOT_SELECTED', 'Not Selected'),
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon')
    ]
    type = models.CharField(
        null=False,
        max_length=200,
        default='NOT_SELECTED',
        choices=MODEL_CHOICES
    )
    
    year=models.IntegerField(
        default=2025,
        validators=[
            MaxValueValidator(2025),
            MinValueValidator(2015)
            ]
    )

    def __str__(self):
        return self.name 
