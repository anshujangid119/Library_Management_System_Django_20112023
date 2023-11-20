from django.db import IntegrityError,DatabaseError
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Book,BookTrasaction,BooksPdf,Fine
from django.utils import timezone
from django.contrib import messages
from django.db.models import F
from .custom_exceptions import InSufficientData
from .forms import BookTrasaction,FeedBackofUser
from django.contrib.auth.hashers import make_password, check_password


@login_required
def home_page(request):
    latest_books = Book.objects.all().order_by('-id')[0:3]
    books = BookTrasaction.objects.filter(user=request.user,return_date=None,is_issued=1)
    total_number = len(books)
    pending_books = BookTrasaction.objects.filter(user=request.user,return_date=None,is_issued=1)
    for i in pending_books:
        delta = i.to_be_return_date - timezone.now().date()
        i.days = delta.days
        i.save()
    near_due_date = BookTrasaction.objects.filter(user=request.user,return_date=None,is_issued=1,days__lte=1)
    return render(request,'home.html', {'book':latest_books,'books_quantity':total_number,'near_due_date':near_due_date})


def signup_page(request):
    if request.method=='POST':
        uname=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['password1']
        pass2=request.POST['password2']
        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:
            try:
                if (uname or email or pass1 or pass2) is None:
                    raise InSufficientData
                else:
                    my_user=User.objects.create_user(uname,email,pass1)
                    my_user.save()
                    user2 = User.objects.get(username=uname)
                    Fine.objects.create(username=user2)
                    return redirect('login') 
            except IntegrityError:
                return HttpResponse("User already exists!")
            except DatabaseError:
                return HttpResponse("Data base connection error")
            except InSufficientData:
                return HttpResponse("Insufficient Input")
            except:
                return HttpResponse("Something Went wrong")
    return render(request,'signup.html')


def login_page(request):
    if request.method=='POST':
        username=request.POST['username']
        pass1=request.POST['pass']
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse("No User of this name exists")
        user = User.objects.get(username=username)
        if user.check_password(pass1):
            user=authenticate(request,username=username,password=pass1)
            if user is None:
                return HttpResponse("You are Blocked you can't access library Contact admin")  
            login(request,user)
            return redirect('home')                     
    return render (request,'login.html')


@login_required
def logout_page(request):
    logout(request)
    return redirect('login')


@login_required
def issue_book(request):
    if request.method == 'POST':
        book_id = request.POST['book_id']
        try:
            if book_id is None:
                raise InSufficientData
        except InSufficientData:
            return HttpResponse("Insufficient Input")
        else:
            book = Book.objects.get(id=book_id) # for getting book Object (id) 
            user = request.user
            BookTrasaction.objects.create(book=book, user=user, issued_date=timezone.now().date()) 
            obj = Book.objects.get(id=book_id) #.update(quantity=F('quantity')-1)
            obj.quantity -=1
            obj.save()
            messages.info(request,f"{book.book_title} Issue Request has been generated successfully")
            return redirect('issue')
    issued_books = BookTrasaction.objects.filter(user=request.user, return_date=None).values_list('book__id')
    books = Book.objects.exclude(id__in=issued_books).filter(quantity__gt=0).order_by('-id')
    return render(request, 'issue.html',{'books':books})


@login_required
def return_book(request):
    if request.method == 'POST':
        book_id = request.POST['book_id']
        try:
            if book_id is None:
                raise InSufficientData
        except InSufficientData:
            return HttpResponse("Insufficient Input")
        else:
            book = Book.objects.get(id=book_id)
            user = request.user
            obj = BookTrasaction.objects.get(book=book,user=user,is_issued=1,return_date=None)
            return_date = timezone.now().date()
            due_days = (obj.to_be_return_date - return_date).days
            obj.save()
            if due_days < 0:
                obj=Fine.objects.get(username=user)
                f=(abs(due_days))*10
                obj.fine+=f
                BookTrasaction.objects.filter(book=book,user=user,is_issued=1,return_date=None).update(book_fine=f,return_date=timezone.now().date())
                obj.save()
            else:
                BookTrasaction.objects.filter(book=book,user=user).update(return_date=timezone.now())
            Book.objects.filter(id=book_id).update(quantity=F('quantity')+1)
            messages.info(request,f"{book.book_title} Returned Successfully")
            return redirect('return')
    books = BookTrasaction.objects.filter(user=request.user,return_date=None,is_issued=1)
    for i in books:
        delta = i.to_be_return_date - timezone.now().date()
        i.days = delta.days
        i.save()
    return render(request, 'return_book.html',{'books':books})


@login_required
def history(request):
    history = BookTrasaction.objects.filter(user=request.user,is_issued=1).order_by('return_date')
    return render(request,'history.html',{'history':history})


def admin_site(request):
    return redirect('admin')  


@login_required
def pending_request(request):
    books = BookTrasaction.objects.filter(user=request.user,is_issued=0)
    return render(request,'pending_issue.html',{'books':books})



@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedBackofUser(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,"FeedBack sent Successfully")
            return redirect('user_feedback')
    else:
        form = FeedBackofUser()
    return render(request, 'feedback_user.html', {'form': form,})


@login_required
def view_pdf(request):
    names = BooksPdf.objects.all()
    return render(request,'view_pdf_file.html',{'names':names})


@login_required
def fine_user(request):
    user = request.user
    f = Fine.objects.filter(username=user)
    fine = 0
    for i in f:
        fine+=i.fine
    items = BookTrasaction.objects.filter(user=user,book_fine__gt=1)
    return render(request,'fine.html',{'fine':fine,'items':items})
