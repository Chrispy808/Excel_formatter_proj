from django.http import request
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *


#GET-------------------------------------------------------------
def index(request):
    request.session.flush()
    return render(request, 'index.html')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    books = Book.objects.all
    context = {
        'user': user,
        'all_books' : books
    }
    return render(request, 'dashboard.html', context)

def user_page(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'user.html', context)

def edit_user(request, User_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'user.html', context)

def item(request, Book_item_name):
    books = Book.objects.filter(item_name=request.session['item_name'])
    context ={

    }
    return render(request, 'item_page.html', context)

def edit_item(request, Book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_book = Book.objects.get(id=Book_id)
    user = User.objects.get(id=request.session['user_id'])
    all_users = User.objects.all()
    #tracking = this_book.users_tracking.filter(request.session['user_id'])
    #not_tracking = this_book.users_tracking.exclude(request.session['user_id'])
    context = {
        'this_book': this_book,
        #'tracking' : tracking,
        #'not_tracking' : not_tracking
        'user' : user,
        'all_users' : all_users
    }
    return render(request, 'item_page.html', context)

def all_items(request, Book_item_name):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        all_books = Book.objects.filter(item_name=Book_item_name)
        this_book = (f"{Book_item_name}")
        context = {
            'all_books' : all_books,
            'this_book' : this_book
        }
        return render(request, 'all_items.html', context)

def locations(request, Book_location):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        all_books = Book.objects.filter(location=Book_location)
        this_book = (f"{Book_location}")
        context = {
            'all_books' : all_books,
            'this_book' : this_book
        }
        return render(request, 'locations.html', context)

def tracked_items(request, User_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        this_user = User.objects.get(id=User_id)
    context = {
        'tracking' : this_user.tracked_books.all(),
        'this_user' : this_user
    }
    return render(request, 'tracked_items.html',context)

#POST-------------------------------------------------------------
def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.registration_Validator(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user= User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw
        )
        request.session['user_id'] = new_user.id
        return redirect('/dashboard')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.login_validator(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    if request.method == "POST":
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/dashboard')

def logout(request):
    request.session.flush()
    return redirect('/')

def delete_all(request):
    if request.method == 'GET':
        return redirect('/')
    else:
        Book.objects.all().delete()
        return redirect('/dashboard')

def change_item(request, Book_id):
    if request.method == 'GET':
        return redirect('/')
    errors = Book.objects.Book_Validator(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect(f"/item/{Book_id}/edit")
    else:
        this_book = Book.objects.get(id=Book_id)
        this_book.barcode = request.POST['barcode']
        this_book.item_name = request.POST['item_name']
        this_book.order_number = request.POST['order_number']
        this_book.days_overdue = request.POST['days_overdue']
        this_book.quantity = request.POST['quantity']
        this_book.location = request.POST['location']
        this_book.location_name = request.POST['location_name']
        this_book.event_name = request.POST['event_name']
        this_book.comments = request.POST['comments']
        this_book.save()
        return redirect('/dashboard')

def delete_item(request, Book_id):
    if request.method == 'GET':
        return redirect('/')
    else:
        this_book = Book.objects.get(id=Book_id)
        this_book.delete()
        return redirect('/dashboard')

def change_user(request, User_id):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.registration_Validator(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect(f"/user/edit/{User_id}")
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user= User.objects.get(id=User_id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.password = hashed_pw
        user.save()
        return redirect('/dashboard')

def track(request, Book_id):
    if request.method == 'GET':
        return redirect('/')
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user= User.objects.get(id=request.session['user_id'])
        this_book = Book.objects.get(id=Book_id)
        this_book.users_tracking.add(user)
        this_book.save()
        return redirect(f"/item/{Book_id}/edit")

def untrack_item_page(request, Book_id):
    if request.method == 'GET':
        return redirect('/')
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user= User.objects.get(id=request.session['user_id'])
        this_book = Book.objects.get(id=Book_id)
        this_book.users_tracking.remove(user)
        this_book.save()
        return redirect(f"/item/{Book_id}/edit")

def untrack_tracked_page(request, Book_id, User_id):
    if request.method == 'GET':
        return redirect('/')
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user= User.objects.get(id=User_id)
        this_book = Book.objects.get(id=Book_id)
        this_book.users_tracking.remove(user)
        this_book.save()
        return redirect(f"/user/{User_id}/tracking")
