from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from .models import Book,BookTrasaction,FeedBackUser,Fine
from django.utils import timezone
from django.contrib import messages
from django.db.models import F
from .custom_exceptions import InSufficientData
from .forms import BookForm,BookTrasaction,AddBoookTransaction,BookPdf


@user_passes_test(lambda u: u.is_superuser)
def return_book_admin(request):
    if request.method == 'POST':
        book_id = request.POST['book_id']
        user = request.POST['user']
        try:
            if book_id is None:
                raise InSufficientData
        except InSufficientData:
            return HttpResponse("Insufficient Input")
        else:
            book = Book.objects.get(id=book_id)
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
            return redirect('return_book_admin')
    books = BookTrasaction.objects.filter(return_date=None,is_issued=1)
    return render(request, 'return_book_admin.html',{'books':books})


@user_passes_test(lambda u: u.is_superuser)
def add_book_pdf(request):
    if request.method == 'POST':
        form = BookPdf(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request,"Book Added Successfully")
            return redirect('add_pdf')
    else:
        form = BookPdf()
    return render(request, 'add_pdf_book.html', {'form': form})



@user_passes_test(lambda u: u.is_superuser)
def feedback_admin(request):
    feedbacks = FeedBackUser.objects.all().order_by('-id')
    return render(request,'feedback_admin.html',{'feedbacks':feedbacks})



@user_passes_test(lambda u: u.is_superuser)
def all_user_fines(request):    
    if request.method == 'POST':
        user_id = request.POST['id']
        user = User.objects.get(id=user_id)
        f = Fine.objects.filter(username=user)
        fine = 0
        for i in f:
            fine+=i.fine
        items = BookTrasaction.objects.filter(user=user,book_fine__gt=1)
        return render(request,'fine.html',{'fine':fine,'items':items})
    users = User.objects.filter(is_superuser=0).order_by('username')
    return render(request,'admin_user_fines.html',{'users':users})



@user_passes_test(lambda u: u.is_superuser)
def user_record(request):
    if request.method == 'POST':
        user_id = request.POST['id']
        user = User.objects.get(id=user_id)
        history = BookTrasaction.objects.filter(user=user,is_issued=1).order_by('return_date')
        return render(request,'history.html',{'history':history})
    users = User.objects.filter(is_superuser=0).order_by('username')
    return render(request,'users_record.html',{'users':users})


@user_passes_test(lambda u: u.is_superuser)
def records(request):
    records = BookTrasaction.objects.filter(return_date=None,is_issued=1)
    return render(request, 'record.html', {'records': records})



@user_passes_test(lambda u: u.is_superuser)
def issue_book_admin(request):
    if request.method == 'POST':
        form = AddBoookTransaction(request.POST)
        if form.is_valid():
            book_name = form.cleaned_data['book']
            # print(book_name)
            s=str(book_name)
            l = s.split(",")
            name = l[0]
            autor = l[1] 
            obj = Book.objects.get(book_title=name,book_author=autor)
            if obj.quantity < 1:
                return HttpResponse("Sorry This book is not Available Right now")
            else:
                Book.objects.filter(book_title=name,book_author=autor).update(quantity=F('quantity')-1)
                form.save()
                messages.info(request,f"{s} Book Issued Successfully")
                return redirect('issue_book_admin')     
    else:
        form = AddBoookTransaction()
    return render(request, 'issue_book_by_admi.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def display_users(request):
    if request.method == 'POST' and 'delete' in request.POST:
        user_id = request.POST['id']
        user = User.objects.filter(id=user_id)
        user.delete()
        messages.info(request,"User Deleted")

    elif request.method =='POST' and 'block' in request.POST:
        user_id = request.POST['id']
        user = User.objects.get(id=user_id)
        if user.is_active==1:
            user.is_active=0
            user.save()
            messages.info(request,f"{user} Blocked Successfully")
        else:
            user.is_active=1
            user.save() 
            messages.info(request,f"{user} UnBlocked Successfully")       
    users = User.objects.filter(is_superuser=0).order_by('username')
    return render(request,'display_users.html',{'users':users})


@user_passes_test(lambda u: u.is_superuser)
def display_books_admin(request):
    if request.method == 'POST' and 'edit' in request.POST:
        quantity = request.POST.get('quantity')
        if quantity!="":
            id = request.POST['book_id']
            book = Book.objects.get(id=id)
            book.quantity = quantity
            book.save()
            messages.info(request,"Book Edited Successfully")
        return redirect('display_book')
    elif request.method == 'POST' and 'detail' in request.POST:
        quantity = request.POST.get('quantity')
        id = request.POST['book_id']
        book = Book.objects.get(id=id)
        books = BookTrasaction.objects.filter(book=book,return_date=None)
        return render(request,'book_issue_detail.html',{'books':books})

    books = Book.objects.all()
    return render(request,'display_books.html',{'books':books})


@user_passes_test(lambda u: u.is_superuser)
def issue_request(request):
    if request.method == 'POST' and 'accept' in request.POST:
        book_id = request.POST['book_id']
        user1 = request.POST['user']
        user2 = User.objects.get(username=user1)
        book = Book.objects.get(id=book_id)
        BookTrasaction.objects.filter(book=book, user=user2).update(is_issued=1)
        issue_request = BookTrasaction.objects.filter(is_issued=0)
        messages.info(request,"Request Accepted Successfully")
        return render(request,'issue_request.html',{'issue_request':issue_request})
    elif request.method == 'POST' and 'delete' in request.POST:
        book_id = request.POST['book_id']
        user1 = request.POST['user']
        user2 = User.objects.get(username=user1)
        book = Book.objects.get(id=book_id)
        obj = BookTrasaction.objects.filter(book=book, user=user2, is_issued=0)
        obj.delete()
        issue_request = BookTrasaction.objects.filter(is_issued=0)
        messages.info(request,"Request Declined")
        return render(request,'issue_request.html',{'issue_request':issue_request})
    else:
        issue_request = BookTrasaction.objects.filter(is_issued=0)
        return render(request,'issue_request.html',{'issue_request':issue_request})
        

@user_passes_test(lambda u: u.is_superuser)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,"Book Added Successfully")
            return redirect('add')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})