# Create your models here.
from django.db import models

from users.models import User

from datetime import date

# Create your models here.

class Account(models.Model):

    TYPES = (
        ('Ahorro', 'Ahorro'),
        ('Nómina', 'Nómina'),
        ('Efectivo', 'Efectivo'),
        ('Crédito', 'Crédito'),
        ('Wallet', 'Wallet'),
        ('Departamental', 'Departamental'),
        ('Vales', 'Vales')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=20)
    account_type = models.CharField(max_length=15, choices=TYPES, null = False, blank=False)
    account_number = models.CharField(max_length=128) 
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, null = False)
    due_date = models.DateField(default=date.today)
    status_delete = models.BooleanField(default=False)


    def __str__(self): 
        return self.user
