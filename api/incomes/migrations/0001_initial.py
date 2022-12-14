# Generated by Django 4.0.3 on 2022-08-08 05:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income_date', models.DateField(default=datetime.date.today)),
                ('income_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('income_description', models.TextField(default='', max_length=50)),
                ('status_delete', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
        ),
    ]
