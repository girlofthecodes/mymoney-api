from django.db import models

from users.models import User 
from accounts.models import Account
from labels.models import Label

from datetime import date

# Create your models here.
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    account = models.ForeignKey(Account, on_delete=models.CASCADE) 
    label = models.ForeignKey(Label, on_delete=models.CASCADE) 
    income_date = models.DateField(default=date.today) 
    income_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    income_description = models.TextField(max_length=50, default="")
    status_delete= models.BooleanField(default=False)

