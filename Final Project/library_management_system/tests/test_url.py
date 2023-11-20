from django.test import SimpleTestCase
from django.urls import resolve,reverse
# from library_management_system.views import home_page,login_page,signup_page,issue_book,return_book,history,add_book,issue_request,pending_request,display_books_admin,display_users,issue_book_admin,records,user_record,feedback,feedback_admin,add_book_pdf,view_pdf,fine_user,all_user_fines,return_book_admin
from library_management_system import admin_views,views
class TestUrls(SimpleTestCase):

    def test_home(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func,views.home_page)

    def test_login(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func,views.login_page)

    def test_signuo(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func,views.signup_page)
    
    def test_issue_book(self):
        url = reverse('issue')
        self.assertEqual(resolve(url).func,views.issue_book)

    def test_return_book(self):
        url = reverse('return')
        self.assertEqual(resolve(url).func,views.return_book)

    def test_history(self):
        url = reverse('history')
        self.assertEqual(resolve(url).func,views.history)
    

    def test_add_book(self):
        url = reverse('add')
        self.assertEqual(resolve(url).func,admin_views.add_book)

    def test_issue_request(self):
        url = reverse('issue_req')
        self.assertEqual(resolve(url).func,admin_views.issue_request)
    
    def test_pending_request(self):
        url = reverse('pending_req')
        self.assertEqual(resolve(url).func,views.pending_request)
    
    def test_display_books_admin(self):
        url = reverse('display_book')
        self.assertEqual(resolve(url).func,admin_views.display_books_admin)

    def test_display_users(self):
        url = reverse('display_users')
        self.assertEqual(resolve(url).func,admin_views.display_users)

    def test_issue_book_admin(self):
        url = reverse('issue_book_admin')
        self.assertEqual(resolve(url).func,admin_views.issue_book_admin)

    def test_records(self):
        url = reverse('records')
        self.assertEqual(resolve(url).func,admin_views.records)
        
    def test_user_record(self):
        url = reverse('user_records')
        self.assertEqual(resolve(url).func,admin_views.user_record)

    def test_feedback(self):
        url = reverse('user_feedback')
        self.assertEqual(resolve(url).func,views.feedback)
    
    def test_feedback_admin(self):
        url = reverse('admin_feedback')
        self.assertEqual(resolve(url).func,admin_views.feedback_admin)

    def test_add_book_pdf(self):
        url = reverse('add_pdf')
        self.assertEqual(resolve(url).func,admin_views.add_book_pdf)

    def test_view_pdf(self):
        url = reverse('view_pdf')
        self.assertEqual(resolve(url).func,views.view_pdf)
    
    def test_fine_user(self):
        url = reverse('fine_user')
        self.assertEqual(resolve(url).func,views.fine_user)

    def test_all_user_fines(self):
        url = reverse('all_user_fine')
        self.assertEqual(resolve(url).func,admin_views.all_user_fines)

    def test_return_book_admin(self):
        url = reverse('return_book_admin')
        self.assertEqual(resolve(url).func,admin_views.return_book_admin)

    