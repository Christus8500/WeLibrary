# Importing required libraries and modules
from datetime import datetime
from random import random
from secrets import choice
from sys import prefix
from unicodedata import category
from django import forms
from numpy import require
from lmsApp import models
from .models import Books, SubCategory, Videos

# Importing Django auth forms and models
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
import datetime


# Form for saving user information, inherits from UserCreationForm
class SaveUser(UserCreationForm):
    # Username field with max length 250 and help text
    username = forms.CharField(max_length=250, help_text="The Username field is required.")
    # Email field with max length 250 and help text
    email = forms.EmailField(max_length=250, help_text="The Email field is required.")
    # First name field with max length 250 and help text
    first_name = forms.CharField(max_length=250, help_text="The First Name field is required.")
    # Last name field with max length 250 and help text
    last_name = forms.CharField(max_length=250, help_text="The Last Name field is required.")
    # Password1 field with max length 250
    password1 = forms.CharField(max_length=250)
    # Password2 field with max length 250
    password2 = forms.CharField(max_length=250)

    class Meta:
        # Associate this form with the User model
        model = User
        # Specify the fields to include in the form
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2',)


# Form for updating user profile, inherits from UserChangeForm
class UpdateProfile(UserChangeForm):
    # Username field with max length 250 and help text
    username = forms.CharField(max_length=250, help_text="The Username field is required.")
    # Email field with max length 250 and help text
    email = forms.EmailField(max_length=250, help_text="The Email field is required.")
    # First name field with max length 250 and help text
    first_name = forms.CharField(max_length=250, help_text="The First Name field is required.")
    # Last name field with max length 250 and help text
    last_name = forms.CharField(max_length=250, help_text="The Last Name field is required.")
    # Current password field with max length 250
    current_password = forms.CharField(max_length=250)

    class Meta:
        # Associate this form with the User model
        model = User
        # Specify the fields to include in the form
        fields = ('email', 'username', 'first_name', 'last_name')

    # Method to clean and validate the current password
    def clean_current_password(self):
        # Check if the current password is correct
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError("Password is Incorrect")

    # Method to clean and validate the email
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            # Exclude the current user and check if the email is already taken
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} email is already exists/taken")

    # Method to clean and validate the username
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            # Exclude the current user and check if the username is already taken
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} username is already exists/taken")


# Form for updating user information, inherits from UserChangeForm
class UpdateUser(UserChangeForm):
    # Username field with max length 250 and help text
    username = forms.CharField(max_length=250, help_text="The Username field is required.")
    # Email field with max length 250 and help text
    email = forms.EmailField(max_length=250, help_text="The Email field is required.")
    # First name field with max length 250 and help text
    first_name = forms.CharField(max_length=250, help_text="The First Name field is required.")
    # Last name field with max length 250 and help text
    last_name = forms.CharField(max_length=250, help_text="The Last Name field is required.")

    class Meta:
        # Associate this form with the User model
        model = User
        # Specify the fields to include in the form
        fields = ('email', 'username', 'first_name', 'last_name')

    # Method to clean and validate the email
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            # Exclude the current user and check if the email is already taken
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} email already exists/taken")

    # Method to clean and validate the username
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            # Exclude the current user and check if the username is already taken
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} username already exists/taken")


# Form for updating passwords, inherits from PasswordChangeForm
class UpdatePasswords(PasswordChangeForm):
    # Field for the old password with custom widget and label
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm rounded-0'}), label="Old Password")

    # Field for the new password with custom widget and label
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm rounded-0'}), label="New Password")

    # Field to confirm the new password with custom widget and label
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm rounded-0'}),
        label="Confirm New Password")

    class Meta:
        # Associate this form with the User model
        model = User
        # Specify the fields to include in the form
        fields = ('old_password', 'new_password1', 'new_password2')


# Form for saving category information, inherits from ModelForm
class SaveCategory(forms.ModelForm):
    # Field for the category name with a maximum length of 250 characters
    name = forms.CharField(max_length=250)
    # Field for the category description as a textarea
    description = forms.Textarea()
    # Field for the category status with a maximum length of 2 characters
    status = forms.CharField(max_length=2)

    class Meta:
        # Associate this form with the Category model
        model = models.Category
        # Specify the fields to include in the form
        fields = ('name', 'description', 'status',)

    def clean_name(self):
        # Retrieve the category ID from the data if it's numeric; otherwise, set it to 0
        id = self.data['id'] if (self.data['id']).isnumeric() else 0
        # Retrieve the cleaned name field data
        name = self.cleaned_data['name']
        try:
            # Check if a category with the same name exists (excluding the current one if ID > 0)
            if id > 0:
                category = models.Category.objects.exclude(id=id).get(name=name, delete_flag=0)
            else:
                category = models.Category.objects.get(name=name, delete_flag=0)
        except:
            # If no such category exists, return the name (validation passed)
            return name
        # Raise a validation error if a category with the same name already exists
        raise forms.ValidationError("Category Name already exists.")


# Form for saving sub-category information, inherits from ModelForm
class SaveSubCategory(forms.ModelForm):
    # Field for the category associated with the sub-category
    category = forms.CharField(max_length=250)
    # Field for the sub-category name with a maximum length of 250 characters
    name = forms.CharField(max_length=250)
    # Field for the sub-category description as a textarea
    description = forms.Textarea()
    # Field for the sub-category status with a maximum length of 2 characters
    status = forms.CharField(max_length=2)

    class Meta:
        # Associate this form with the SubCategory model
        model = models.SubCategory
        # Specify the fields to include in the form
        fields = ('category', 'name', 'description', 'status',)

    def clean_category(self):
        # Retrieve the category ID from the data and convert it to an integer (if numeric)
        cid = int(self.data['category']) if (self.data['category']).isnumeric() else 0
        try:
            # Attempt to get the category object with the given ID
            category = models.Category.objects.get(id=cid)
            # Return the category object if found
            return category
        except:
            # Raise a validation error if the category is invalid (not found)
            raise forms.ValidationError("Invalid Category.")

    def clean_name(self):
        # Retrieve the ID of the sub-category (convert to an integer if numeric; otherwise, set to 0)
        id = int(self.data['id']) if (self.data['id']).isnumeric() else 0
        # Retrieve the ID of the category associated with the sub-category
        cid = int(self.data['category']) if (self.data['category']).isnumeric() else 0
        # Retrieve the cleaned name field data
        name = self.cleaned_data['name']
        try:
            # Retrieve the category object based on the category ID
            category = models.Category.objects.get(id=cid)
            # Check if a sub-category with the same name already exists under the same category
            if id > 0:
                sub_category = models.SubCategory.objects.exclude(id=id).get(name=name, delete_flag=0,
                                                                             category=category)
            else:
                sub_category = models.SubCategory.objects.get(name=name, delete_flag=0, category=category)
        except:
            # If no such sub-category exists, return the name (validation passed)
            return name
        # Raise a validation error if a sub-category with the same name already exists under the selected category
        raise forms.ValidationError("Sub-Category Name already exists on the selected Category.")


# Form for saving book information, inherits from ModelForm
class SaveBook(forms.ModelForm):
    class Meta:
        model = Books
        # Specify the fields to include in the form
        fields = (
            'isbn', 'sub_category', 'title', 'description', 'author', 'publisher', 'date_published', 'file', 'cover_image', 'download', 'status'
        )

    def __init__(self, *args, **kwargs):
        # Initialize the form with custom behaviors
        super(SaveBook, self).__init__(*args, **kwargs)
        # Check if the instance exists and has a primary key (if it's an update operation)
        if self.instance and self.instance.pk:
            # Set the 'file' and 'cover_image' fields as not required if updating
            self.fields['file'].required = False
            self.fields['cover_image'].required = False

    def clean_sub_category(self):
        # Retrieve the sub-category ID from the data and convert it to an integer (if numeric)
        scid = int(self.data['sub_category']) if self.data['sub_category'].isnumeric() else 0
        try:
            # Attempt to retrieve the sub-category object with the given ID
            sub_category = SubCategory.objects.get(id=scid)
            # Return the sub-category object if found
            return sub_category
        except SubCategory.DoesNotExist:
            # Raise a validation error if the sub-category is invalid (not found)
            raise forms.ValidationError("Invalid Sub Category.")

    def clean_isbn(self):
        # Retrieve the ID of the book (convert to an integer if numeric; otherwise, set to 0)
        id = int(self.data['id']) if self.data['id'].isnumeric() else 0
        # Retrieve the cleaned ISBN field data
        isbn = self.cleaned_data['isbn']
        try:
            # Check if a book with the same ISBN already exists in the database
            if id > 0:
                book = Books.objects.exclude(id=id).get(isbn=isbn, delete_flag=0)
            else:
                book = Books.objects.get(isbn=isbn, delete_flag=0)
        except Books.DoesNotExist:
            # If no such book exists, return the ISBN (validation passed)
            return isbn
        # Raise a validation error if a book with the same ISBN already exists in the database
        raise forms.ValidationError("ISBN already exists in the database.")


# Form for saving video information, inherits from ModelForm
class SaveVideo(forms.ModelForm):
    class Meta:
        model = Videos
        # Specify the fields to include in the form
        fields = ('sub_category', 'title', 'description', 'status', 'video_file', 'thumbnail_image', 'download')

    def __init__(self, *args, **kwargs):
        # Initialize the form with custom behaviors
        super(SaveVideo, self).__init__(*args, **kwargs)
        # Check if the instance exists and has a primary key (if it's an update operation)
        if self.instance and self.instance.pk:
            # Set the 'video_file' and 'thumbnail_image' fields as not required if updating
            self.fields['video_file'].required = False
            self.fields['thumbnail_image'].required = False

    def clean_sub_category(self):
        # Retrieve the sub-category ID from the data (default to 0 if not found)
        scid = int(self.data.get('sub_category', 0))
        try:
            # Attempt to retrieve the sub-category object with the given ID
            return SubCategory.objects.get(id=scid)
        except SubCategory.DoesNotExist:
            # Raise a validation error if the sub-category is invalid (not found)
            raise forms.ValidationError("Invalid Sub Category.")


# Form for saving student information, inherits from ModelForm
class SaveStudent(forms.ModelForm):
    # Define form fields for student information
    code = forms.CharField(max_length=250)
    first_name = forms.CharField(max_length=250)
    middle_name = forms.CharField(max_length=250, required=False)
    last_name = forms.CharField(max_length=250)
    gender = forms.CharField(max_length=250)
    contact = forms.CharField(max_length=250)
    email = forms.CharField(max_length=250)
    department = forms.CharField(max_length=250)
    course = forms.CharField(max_length=250)
    address = forms.Textarea()
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.Students
        # Specify the fields to include in the form
        fields = (
            'code', 'first_name', 'middle_name', 'last_name', 'gender', 'contact', 'email', 'address', 'department',
            'course', 'status',)

    def clean_code(self):
        # Retrieve the student ID from the data (default to 0 if not found)
        id = int(self.data['id']) if (self.data['id']).isnumeric() else 0
        code = self.cleaned_data['code']
        try:
            # Check if a student with the same code exists in the database
            if id > 0:
                book = models.Books.objects.exclude(id=id).get(code=code, delete_flag=0)
            else:
                book = models.Books.objects.get(code=code, delete_flag=0)
        except:
            return code
        # Raise a validation error if the student code already exists in the database
        raise forms.ValidationError("Student School Id already exists on the Database.")


# Form for saving Borrowing Transactions information, inherits from ModelForm
class SaveBorrow(forms.ModelForm):
    # Define form fields for borrowing information
    student = forms.CharField(max_length=250)
    book = forms.CharField(max_length=250)
    borrowing_date = forms.DateField()
    return_date = forms.DateField()
    status = forms.CharField(max_length=2)

    class Meta:
        model = models.Borrow
        # Specify the fields to include in the form
        fields = ('student', 'book', 'borrowing_date', 'return_date', 'status',)

    def clean_student(self):
        # Retrieve the student ID from the data (default to 0 if not found)
        student = int(self.data['student']) if (self.data['student']).isnumeric() else 0
        try:
            # Check if the student with the given ID exists in the database
            student = models.Students.objects.get(id=student)
            return student
        except:
            # Raise a validation error if the student is invalid
            raise forms.ValidationError("Invalid student.")

    def clean_book(self):
        # Retrieve the book ID from the data (default to 0 if not found)
        book = int(self.data['book']) if (self.data['book']).isnumeric() else 0
        try:
            # Check if the book with the given ID exists in the database
            book = models.Books.objects.get(id=book)
            return book
        except:
            # Raise a validation error if the book is invalid
            raise forms.ValidationError("Invalid Book.")


# Form for saving inquiry information, inherits from ModelForm
class SaveInquiry(forms.ModelForm):
    # Define form fields for inquiry information
    name = forms.CharField(max_length=250)
    email = forms.CharField(max_length=250)
    topic = forms.CharField(max_length=250)
    message = forms.Textarea()

    class Meta:
        model = models.Inquiry
        # Specify the fields to include in the form
        fields = ('name', 'email', 'topic', 'message',)

