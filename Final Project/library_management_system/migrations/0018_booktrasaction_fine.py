# Generated by Django 4.1.7 on 2023-03-26 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_management_system', '0017_fine'),
    ]

    operations = [
        migrations.AddField(
            model_name='booktrasaction',
            name='fine',
            field=models.IntegerField(default=0),
        ),
    ]
