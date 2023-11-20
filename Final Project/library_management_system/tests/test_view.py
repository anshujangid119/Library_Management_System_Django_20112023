from django.utils import timezone
from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from library_management_system.models import Book,BookTrasaction


class TestView(TestCase):

    def setUp(self):
        self.username = 'test1'
        self.password = '1234'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.book_title = 'unit testing'
        self.book_author = 'tester'
        self.quantity = 10
        self.client.login(username=self.username, password=self.password,is_superuser=1)
        self.book = Book.objects.create(book_title=self.book_title,book_author=self.book_author,quantity=self.quantity)
    
    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(authenticate(username=self.username, password=self.password))
        # self.assertTemplateUsed(response,'login.html')

    def test_signup(self):
        data = {'username': 'test2', 'email': 'tset2@gmail.com','password1':1234,'password2':1234}
        response = self.client.post(reverse('signup'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.get(username="test2"))
        # self.assertTemplateUsed(response,'signup.html')

    def test_login_page(self):
        data = {'username':'test1','pass': '1234'}
        response = self.client.post(reverse('login'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(authenticate(username=self.username, password=self.password))
        # self.assertTemplateUsed(response,'login.html')


class IssueViwe(TestCase):
    def setUp(self):
        self.username = 'test1'
        self.password = '1234'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.book_title = 'unit testing'
        self.book_author = 'tester'
        self.quantity = 10
        self.client.login(username=self.username, password=self.password,is_superuser=1)
        self.book = Book.objects.create(book_title=self.book_title,book_author=self.book_author,quantity=self.quantity)
             

    def test_issue_book(self):
        data = {'book_id':self.book.id}
        response = self.client.post(reverse('issue'), data=data)
        self.assertEqual(response.status_code, 302)
        obj = Book.objects.get(id=self.book.id)
        self.assertEqual(obj.quantity,self.quantity-1)
        self.assertTrue(User.objects.get(username=self.username))
        BookTrasaction.objects.create(issued_date=timezone.now(),book=self.book,user=self.user)
        self.assertTrue(BookTrasaction.objects.filter(issued_date=timezone.now(),book=self.book,user=self.user))


class ReturnView(TestCase):
    def setUp(self):
        self.username = 'test2'
        self.password = '1234'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.book_title = 'unit testing2'
        self.book_author = 'tester'
        self.quantity = 10
        self.client.login(username=self.username, password=self.password,is_superuser=1)
        self.book = Book.objects.create(book_title=self.book_title,book_author=self.book_author,quantity=self.quantity)
        BookTrasaction.objects.create(issued_date=timezone.now(),book=self.book,user=self.user,is_issued=1)

    def test_return_book(self):
        data = {'book_id':self.book.id}
        response = self.client.post(reverse('return'), data=data)
        self.assertEqual(response.status_code, 302)
        obj = Book.objects.get(id=self.book.id)
        self.assertTrue(BookTrasaction.objects.filter(issued_date=timezone.now(),book=self.book,user=self.user,return_date=timezone.now()))
        self.assertEqual(obj.quantity,11)
    

class IssueRequset(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(book_title='Test Book', book_author='Test Author',quantity=10)
        self.book_transaction = BookTrasaction.objects.create(
        issued_date=timezone.now().date(),
        book=self.book,
        user=self.user
    )
    def test_accept_request(self):
        data = {'book_id':self.book.id,'user':self.user,'accept':True}
        response = self.client.post(reverse('issue_req'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BookTrasaction.objects.filter(book=self.book,user=self.user))

    def test_decline_request(self):
        data = {'book_id':self.book.id,'user':self.user,'accept':False}
        response = self.client.post(reverse('issue_req'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BookTrasaction.objects.filter(issued_date=timezone.now(),book=self.book,user=self.user,is_issued=1))
