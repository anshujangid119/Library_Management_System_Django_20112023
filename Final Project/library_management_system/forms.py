from django import forms
from .models import Book,BookTrasaction,FeedBackUser,BooksPdf

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('__all__')
class EditBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['id','quantity']
class AddBoookTransaction(forms.ModelForm):
    class Meta:
        model = BookTrasaction
        exclude = ('return_date',)
class FeedBackofUser(forms.ModelForm):
    class Meta:
        model = FeedBackUser
        fields = ('__all__')
class BookPdf(forms.ModelForm):
    class Meta:
        model = BooksPdf
        fields = ('__all__')