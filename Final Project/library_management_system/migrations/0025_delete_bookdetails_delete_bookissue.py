# Generated by Django 4.1.7 on 2023-03-29 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_management_system', '0024_bookdetails'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BookDetails',
        ),
        migrations.DeleteModel(
            name='BookIssue',
        ),
    ]
