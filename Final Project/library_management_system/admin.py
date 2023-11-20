from django.contrib import admin
from .models import Book,User,BookTrasaction

admin.site.site_header = 'Library Management System'
admin.site.site_title = 'Library Management System'
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['book_title','book_author','quantity']
    search_fields = ['book_title','book_author','quantity']

@admin.register(BookTrasaction)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ['user','book','issued_date','return_date','to_be_return_date']
    list_filter = ['user','book','issued_date','return_date','to_be_return_date']
    list_per_page = 10
