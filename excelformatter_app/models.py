from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def registration_Validator(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'
        if len(form['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"
        if len(form['password']) < 5:
            errors['password'] = 'Password must be at least 5 characters'
        if form['password'] != form['confirm_password']:
            errors['password'] = 'Passwords do not match'
        return errors

    def login_validator(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

class BookManager(models.Manager):
    def Book_Validator(self, form):
        errors = {}
        if len(form['barcode']) == 0:
            errors['barcode'] = 'Barcode field must not be empty'
        if len(form['item_name']) == 0:
            errors['item_name'] = 'Item Name field must not be empty'
        if len(form['order_number']) == 0:
            errors['order_number'] = 'Order Number field must not be empty'
        if len(form['days_overdue']) == 0:
            errors['days_overdue'] == 'Days Overdue field must not be empty'
        if len(form['quantity']) == 0:
            errors['quantity'] = 'Quantity field must not be empty'
        if len(form['location']) == 0:
            errors['location'] == 'Location field must not be empty'
        if len(form['location_name']) == 0:
            errors['location_name'] == 'Location Name field must not be empty'
        if len(form['event_name']) == 0:
            errors['event_name'] == 'Event Name field must not be empty'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return self.first_name

class Book(models.Model):
    barcode = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    order_number = models.IntegerField()
    days_overdue = models.IntegerField()
    quantity = models.IntegerField()
    location = models.IntegerField()
    location_name = models.CharField(max_length=255)
    event_name = models.CharField(max_length=255)
    comments = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
    users_tracking = models.ManyToManyField(User, related_name="tracked_books")

    def __repr__(self):
        return self.item_name