# Generated by Django 4.1.7 on 2023-04-13 08:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_management_system', '0029_booktrasaction_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
