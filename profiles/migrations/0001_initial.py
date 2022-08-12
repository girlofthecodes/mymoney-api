# Generated by Django 4.0.3 on 2022-08-08 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('middle_name', models.CharField(max_length=20)),
                ('first_surname', models.CharField(max_length=20)),
                ('second_surname', models.CharField(max_length=20)),
                ('birth_date', models.DateField()),
                ('age', models.IntegerField(default=0)),
                ('place_of_birth', models.CharField(max_length=30)),
                ('residence_place', models.CharField(max_length=30)),
                ('residence_country', models.CharField(max_length=30)),
                ('status_delete', models.BooleanField(default=False)),
            ],
        ),
    ]
