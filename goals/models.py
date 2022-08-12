from django.db import models

from datetime import date 

from users.models import User

from datetime import date

# Create your models here.
class Goal(models.Model): 
    TYPES = (
        ('Diario', 'Diario'),
        ('Semanal', 'Semanal'), 
        ('Quincenal', 'Quincenal'), 
        ('Mensual', 'Mensual')
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
    goal_concept = models.TextField(max_length=50)
    start_date = models.DateField(default=date.today) 
    due_date = models.DateField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    goal_period = models.CharField(max_length=20, choices=TYPES, null=False, blank=False)
    goal_total = models.DecimalField(max_digits=10, decimal_places=2, default= 0) 
    goal_color = models.CharField(max_length=8, choices=COLOR_CHOICES, null=False, blank=False)
    status_delete = models.BooleanField(default=False)
