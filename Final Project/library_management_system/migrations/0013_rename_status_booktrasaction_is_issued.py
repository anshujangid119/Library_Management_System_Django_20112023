# Generated by Django 4.1.7 on 2023-03-17 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_management_system', '0012_booktrasaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booktrasaction',
            old_name='status',
            new_name='is_issued',
        ),
    ]
