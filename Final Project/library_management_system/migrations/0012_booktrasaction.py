# Generated by Django 4.1.7 on 2023-03-17 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import library_management_system.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library_management_system', '0011_alter_book_book_author_alter_book_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookTrasaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issued_date', models.DateField()),
                ('return_date', models.DateField(null=True)),
                ('to_be_return_date', models.DateField(default=library_management_system.models.default_return_date)),
                ('status', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_management_system.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
