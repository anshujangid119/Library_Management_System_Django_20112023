# Generated by Django 4.1.7 on 2023-03-27 04:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_management_system', '0020_alter_booktrasaction_issued_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booktrasaction',
            name='fine',
        ),
        migrations.DeleteModel(
            name='Fine',
        ),
    ]