from django.db import models

from users.models import User 
from accounts.models import Account
from labels.models import Label

from datetime import date


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "user") #Se cambio
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name = "account") 
    label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name = "label") 

    expense_description = models.TextField(max_length=50) #Descripcion, puede ser opcional
    expense_date = models.DateField(default=date.today) #Dia del gasto
    expense_amount = models.DecimalField(max_digits=10, decimal_places=2, null = False) #Importe del gasto
    
    status_delete = models.BooleanField(default=False)


