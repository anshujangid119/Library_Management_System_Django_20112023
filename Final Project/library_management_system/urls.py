from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views,admin_views
urlpatterns = [
    path('',views.signup_page,name='signup'),
    path('login/',views.login_page,name='login'),
    path('home/',views.home_page,name='home'),
    path('logout/',views.logout_page,name='logout'),
    path('issue/',views.issue_book,name='issue'),
    path('return/',views.return_book,name='return'),
    path('history/',views.history,name='history'),
    path('admin/',views.admin_site,name= 'admin'),
    path('add_book/',admin_views.add_book,name='add'),
    path('issue_req/',admin_views.issue_request,name='issue_req'),
    path('pending_req/',views.pending_request,name='pending_req'),
    path('display_books/',admin_views.display_books_admin,name='display_book'),
    path('users/', admin_views.display_users, name='display_users'),
    path('issue_book_admin/',admin_views.issue_book_admin,name='issue_book_admin'),
    path('record/', admin_views.records, name='records'),
    path('user_record/', admin_views.user_record, name='user_records'),
    path('user_feedback/',views.feedback,name='user_feedback'),
    path('feedback_admin/',admin_views.feedback_admin,name='admin_feedback'),
    path('add_book_pdf/',admin_views.add_book_pdf,name='add_pdf'),
    path('view_pdf/',views.view_pdf,name='view_pdf'),
    path('fine/',views.fine_user,name='fine_user'),
    path('users_fine/',admin_views.all_user_fines,name='all_user_fine'),
    path('return_admin/',admin_views.return_book_admin,name='return_book_admin'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)