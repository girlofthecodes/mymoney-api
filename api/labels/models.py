from django.db import models
from users.models import User

# Create your models here.

class Label(models.Model):
    TYPE_CHOICES = (
        ('Gasto', 'Gasto'), 
        ('Ingreso', 'Ingreso'), 
    )
    CLASS_CHOICES = (
        ('Fijo', 'Fijo'), 
        ('Variable', 'Variable'), 
    )
    COLOR_CHOICES = (
        ('Azul', 'Azul'),
        ('Verde', 'Verde'),
        ('Amarillo', 'Amarillo'),
        ('Rojo', 'Rojo'),
        ('Naranja', 'Naranja'),
        ('Morado', 'Morado'),
        ('Rosa', 'Rosa')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    label_name = models.CharField(max_length=20)
    label_type = models.CharField(max_length=12, choices=TYPE_CHOICES, null = False)
    label_class = models.CharField(max_length=10, choices=CLASS_CHOICES, null = False)
    label_color = models.CharField(max_length=8, choices=COLOR_CHOICES)   
    label_description = models.TextField(max_length=100)
    status_delete= models.BooleanField(default=False)