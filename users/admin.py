from django.contrib import admin
from users.models import User
from accounts.models import Account
from labels.models import Label
from expenses.models import Expense

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Label)
admin.site.register(Expense)


