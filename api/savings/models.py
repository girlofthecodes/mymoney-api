from django.db import models

from users.models import User
from goals.models import Goal

from datetime import date

# Create your models here.
class Saving(models.Model): 
    CHOICES = (
        ('Viaje', 'Viaje'), 
        ('Pago deudas', 'Pago deudas'), 
        ('Enganche', 'Enganche'), 
        ('Compra','Compra'),
        ('Otro','Otro')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE) 
    saving_list = models.CharField(max_length=15,choices=CHOICES, null=False, blank=False) 
    saving_date = models.DateField(default=date.today) 
    saving_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False) 
    saving_concept = models.TextField(max_length=50) 
    status_delete = models.BooleanField(default=False) 
