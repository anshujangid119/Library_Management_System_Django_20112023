# Generated by Django 4.1.7 on 2023-02-26 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_management_system', '0004_remove_book_book_quantity_book_avilable_bookissue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookissue',
            name='issued_date',
            field=models.DateField(),
        ),
    ]
