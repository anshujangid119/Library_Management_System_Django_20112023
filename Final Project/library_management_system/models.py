from django.db import models 
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
class Book(models.Model):
    book_title = models.CharField(max_length=200)
    book_author = models.CharField(max_length=100)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    class Meta:
        unique_together = ['book_title','book_author']
    
    def __str__(self):
        return f'{self.book_title},{self.book_author}'
def default_return_date():
    return date.today() + timedelta(days=14)

def issue_data():
    return date.today()+ timedelta(days=0)

class BookTrasaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issued_date = models.DateField(default=issue_data)
    return_date = models.DateField(null=True) 
    to_be_return_date=models.DateField(default=default_return_date)
    is_issued = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(1)])
    book_fine = models.IntegerField(default=0)
    days = models.IntegerField(default=0)
 

class FeedBackUser(models.Model):
    text = models.TextField(max_length=200)

class BooksPdf(models.Model):
    name = models.CharField(max_length=200)
    document = models.FileField(upload_to='documents/')

class Fine(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    fine=models.IntegerField(default=0)
