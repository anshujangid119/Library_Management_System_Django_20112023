from library_management_system.forms import BookForm,EditBookForm,AddBoookTransaction,FeedBackofUser,BookPdf
from django.test import TestCase
from library_management_system.models import Book
from django.contrib.auth.models import User
from django.utils import timezone

class TestBookForm(TestCase):

    def test_book_title_required(self):
        form = BookForm(data={'book_author': 'Unknown', 'quantity': 5})
        self.assertFalse(form.is_valid())

    def test_book_title_max_length(self):
        form = BookForm(data={'book_title': 'a' * 201, 'book_author': 'Unknown', 'quantity': 5})
        self.assertFalse(form.is_valid())
        
    def test_form_submission(self):
        form = BookForm(data={'book_title': 'Testing of Forms', 'book_author': 'Unknown', 'quantity': 5})
        self.assertTrue(form.is_valid())
        book = form.save()
        self.assertEqual(book.book_title, 'Testing of Forms')
        self.assertEqual(book.book_author, 'Unknown')
        self.assertEqual(book.quantity, 5)


class TestAddBoookTransaction(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='1234')
        self.book = Book.objects.create(book_title='Test Book', book_author='Test Author',quantity=10)

    def test_book_transaction(self):
        form = AddBoookTransaction(data={
            'user':self.user,
            'book':self.book,
            'issued_date':timezone.datetime.now(),
            'to_be_return_date':timezone.datetime.now(),
            'is_issued':1,
            'book_fine':0
        })
        self.assertTrue(form.is_valid())
        trans = form.save()
        self.assertEqual(trans.user,self.user)


class TestFeedBackofUser(TestCase):

    def test_feed_back_form(self):
        form = FeedBackofUser(data={
            'text':'HI this is testing'
        })
        feedback = form.save()
        self.assertEqual(feedback.text,'HI this is testing')

    def test_max_length(self):
        form = BookForm(data={'text': 'a' * 201})
        self.assertFalse(form.is_valid())
    