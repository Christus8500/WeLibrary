import datetime
from django.shortcuts import redirect, render, get_object_or_404
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from lmsApp import models, forms
from .forms import SaveVideo
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Videos


# Create your views here.
def context_data(request):
    fullpath = request.get_full_path()  # Get the full path of the request
    abs_uri = request.build_absolute_uri()  # Get the absolute URI of the request
    abs_uri = abs_uri.split(fullpath)[0]  # Extract the base URI
    context = {
        'system_host': abs_uri,  # Base URI of the system
        'page_name': '',  # Placeholder for the page name
        'page_title': '',  # Placeholder for the page title
        'system_name': 'WE-Library',  # Name of the system
        'topbar': True,  # Display the topbar by default
        'footer': True,  # Display the footer by default
    }
    return context  # Return the context dictionary


def userregister(request):
    context = context_data(request)  # Get the context data
    context['page_title'] = "User Registration"  # Set the page title
    if request.user.is_authenticated:  # Check if the user is authenticated
        return redirect("home-page")  # Redirect to home page if authenticated
    return render(request, 'register.html', context)  # Render the registration page with context


def save_register(request):
    resp = {'status': 'failed', 'msg': ''}  # Initialize response
    if not request.method == 'POST':  # Check if the request method is POST
        resp['msg'] = "No data has been sent on this request"  # Set error message for non-POST requests
    else:
        form = forms.SaveUser(request.POST)  # Initialize the user form with POST data
        if form.is_valid():  # Check if the form is valid
            form.save()  # Save the form data
            messages.success(request, "Your Account has been created successfully")  # Success message
            resp['status'] = 'success'  # Update response status
        else:
            for field in form:  # Iterate over form fields
                for error in field.errors:  # Iterate over field errors
                    if resp['msg'] != '':
                        resp['msg'] += str('<br />')
                    resp['msg'] += str(f"[{field.name}] {error}.")  # Append error messages to response

    return HttpResponse(json.dumps(resp), content_type="application/json")  # Return response as JSON


# Ensures the user is logged in to access this view
@login_required
def update_profile(request):
    context = context_data(request)  # Get the context data
    context['page_title'] = 'Update Profile'  # Set the page title
    user = User.objects.get(id=request.user.id)  # Get the current user
    if not request.method == 'POST':  # Check if the request method is not POST
        form = forms.UpdateProfile(instance=user)  # Initialize the profile update form with user instance
        context['form'] = form  # Add the form to context
    else:
        form = forms.UpdateProfile(request.POST, instance=user)  # Initialize the form with POST data and user instance
        if form.is_valid():  # Check if the form is valid
            form.save()  # Save the form data
            messages.success(request, "Profile has been updated")  # Success message
            return redirect("profile-page")  # Redirect to profile page
        else:
            context['form'] = form  # Add the form with errors to context

    return render(request, 'manage_profile.html', context)  # Render the profile management page with context


@login_required
def update_password(request):
    # Initialize context data for the template
    context = context_data(request)
    context['page_title'] = "Update Password"

    # Check if the request is a POST (form submission)
    if request.method == 'POST':
        # Initialize the form with the POST data and the current user
        form = forms.UpdatePasswords(user=request.user, data=request.POST)

        # Validate the form
        if form.is_valid():
            # Save the new password
            form.save()
            messages.success(request, "Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)  # Update the session hash to keep the user logged in
            return redirect("profile-page")
        else:
            # If the form is not valid, add it to the context to show errors
            context['form'] = form
    else:
        # If the request is not POST, create a blank form
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form

    return render(request, 'update_password.html', context)


def login_page(request):
    # Redirect to home page if the user is already authenticated
    if request.user.is_authenticated:
        return redirect("home-page")

    # Initialize context data for the template
    context = context_data(request)
    context['page_name'] = 'login'
    context['page_title'] = 'Login'

    # Render the login page with the context data
    return render(request, 'login.html', context)


def login_user(request):
    # Log out any currently logged-in user
    logout(request)

    # Initialize response dictionary
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''

    if request.POST:
        # Get username and password from the POST data
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Check if the user account is active
            if user.is_active:
                # Log in the user
                login(request, user)
                resp['status'] = 'success'
            else:
                # Set error message for inactive account
                resp['msg'] = "Incorrect username or password"
        else:
            # Set error message for invalid credentials
            resp['msg'] = "Incorrect username or password"

    # Return the response as JSON
    return HttpResponse(json.dumps(resp), content_type='application/json')


def home(request):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'home'
    context['page_title'] = 'Home'

    # Count various entities and add to context
    context['categories'] = models.Category.objects.filter(delete_flag=0, status=1).all().count()
    context['sub_categories'] = models.SubCategory.objects.filter(delete_flag=0, status=1).all().count()
    context['students'] = models.Students.objects.filter(delete_flag=0, status=1).all().count()
    context['users'] = models.User.objects.all().count()
    context['books'] = models.Books.objects.filter(delete_flag=0, status=1).all().count()
    context['videos'] = models.Videos.objects.filter(delete_flag=0, status=1).all().count()
    context['pending'] = models.Borrow.objects.filter(status=1).all().count()
    context['transactions'] = models.Borrow.objects.all().count()
    context['inquiries'] = models.Inquiry.objects.all().count()

    # Render the home page with the context data
    return render(request, 'home.html', context)


def logout_user(request):
    # Log out the current user
    logout(request)
    # Redirect to the home page
    return redirect('home-page')


@login_required
def profile(request):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'profile'
    context['page_title'] = "Profile"

    # Render the profile page with the context data
    return render(request, 'profile.html', context)


@login_required
def users(request):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'users'
    context['page_title'] = "User List"

    # Exclude the current user and superusers from the user list
    context['users'] = User.objects.exclude(pk=request.user.pk).filter(is_superuser=False).all()

    # Render the users page with the context data
    return render(request, 'users.html', context)


def save_user(request):
    # Initialize response dictionary with default values
    # 'status': 'failed' - default status indicating failure
    # 'msg': '' - default empty message to hold error or success messages
    resp = {'status': 'failed', 'msg': ''}

    # Check if the request method is POST
    if request.method == 'POST':
        post = request.POST

        # Check if updating an existing user or creating a new one
        if not post['id'] == '':
            user = User.objects.get(id=post['id'])
            form = forms.UpdateUser(request.POST, instance=user)
        else:
            form = forms.SaveUser(request.POST)

        # Validate the form
        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "User has been saved successfully.")
            else:
                messages.success(request, "User has been updated successfully.")
            resp['status'] = 'success'
        else:
            # Collect form errors
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        resp['msg'] = "There's no data sent on the request"

    # Return response as JSON
    return HttpResponse(json.dumps(resp), content_type="application/json")


def manage_user(request, pk=None):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'manage_user'
    context['page_title'] = 'Manage User'

    # Check if managing an existing user or creating a new one
    if pk is None:
        context['user'] = {}
    else:
        context['user'] = User.objects.get(id=pk)

    # Render the manage user page with the context data
    return render(request, 'manage_user.html', context)


@login_required
def delete_user(request, pk=None):
    # Initialize response dictionary with default values
    resp = {'status': 'failed', 'msg': ''}

    # Check if a valid user ID is provided
    if pk is None:
        resp['msg'] = 'User ID is invalid'
    else:
        try:
            # Attempt to delete the user with the given primary key (ID)
            User.objects.filter(pk=pk).delete()
            # If successful, display a success message
            messages.success(request, "User has been deleted successfully.")
            # Update the response status to 'success'
            resp['status'] = 'success'
        except:
            # If an error occurs, set the error message
            resp['msg'] = "Deleting User Failed"

    # Return response as JSON
    return HttpResponse(json.dumps(resp), content_type="application/json")


def category(request):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'category'
    context['page_title'] = "Category List"

    # Get all active categories
    context['category'] = models.Category.objects.filter(delete_flag=0).all()

    # Render the category page with the context data
    return render(request, 'category.html', context)


def save_category(request):
    resp = {'status': 'failed', 'msg': ''}

    # Check if the request method is POST
    if request.method == 'POST':
        post = request.POST

        # Check if updating an existing category or creating a new one
        if not post['id'] == '':
            category = models.Category.objects.get(id=post['id'])
            form = forms.SaveCategory(request.POST, instance=category)
        else:
            form = forms.SaveCategory(request.POST)

        # Validate the form
        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Category has been saved successfully.")
            else:
                messages.success(request, "Category has been updated successfully.")
            resp['status'] = 'success'
        else:
            # Collect form errors
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        resp['msg'] = "There's no data sent on the request"

    # Return response as JSON
    return HttpResponse(json.dumps(resp), content_type="application/json")


def view_category(request, pk=None):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'view_category'
    context['page_title'] = 'View Category'

    # Check if a primary key (ID) is provided
    if pk is None:
        # If no ID is provided, set category context to an empty dictionary
        context['category'] = {}
    else:
        # If an ID is provided, retrieve the category with the given ID
        context['category'] = models.Category.objects.get(id=pk)

    # Render the view category page with the context data
    return render(request, 'view_category.html', context)


def manage_category(request, pk=None):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'manage_category'
    context['page_title'] = 'Manage Category'

    # Check if a primary key (ID) is provided
    if pk is None:
        # If no ID is provided, set category context to an empty dictionary
        context['category'] = {}
    else:
        # If an ID is provided, retrieve the category with the given ID
        context['category'] = models.Category.objects.get(id=pk)

    # Render the manage category page with the context data
    return render(request, 'manage_category.html', context)


def delete_category(request, pk=None):
    # Initialize response dictionary with default values
    resp = {'status': 'failed', 'msg': ''}

    # Check if a valid category ID is provided
    if pk is None:
        resp['msg'] = 'Category ID is invalid'
    else:
        try:
            # Mark the category as deleted by setting the delete_flag to 1
            models.Category.objects.filter(pk=pk).update(delete_flag=1)
            # If successful, display a success message
            messages.success(request, "Category has been deleted successfully.")
            # Update the response status to 'success'
            resp['status'] = 'success'
        except:
            # If an error occurs, set the error message
            resp['msg'] = "Deleting Category Failed"

    # Return response as JSON
    return HttpResponse(json.dumps(resp), content_type="application/json")


def sub_category(request):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'sub_category'
    context['page_title'] = "Sub Category List"

    # Get all active subcategories
    context['sub_category'] = models.SubCategory.objects.filter(delete_flag=0).all()

    # Render the subcategory list page with the context data
    return render(request, 'sub_category.html', context)


def save_sub_category(request):
    # Initialize response dictionary with default values
    resp = {'status': 'failed', 'msg': ''}

    # Check if the request method is POST
    if request.method == 'POST':
        post = request.POST

        # Check if updating an existing sub-category or creating a new one
        if not post['id'] == '':
            sub_category = models.SubCategory.objects.get(id=post['id'])
            form = forms.SaveSubCategory(request.POST, instance=sub_category)
        else:
            form = forms.SaveSubCategory(request.POST)

        # Validate the form
        if form.is_valid():
            form.save()
            if post['id'] == '':
                messages.success(request, "Sub Category has been saved successfully.")
            else:
                messages.success(request, "Sub Category has been updated successfully.")
            resp['status'] = 'success'
        else:
            # Collect form errors
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        # Set error message if request method is not POST
        resp['msg'] = "There's no data sent on the request"

    # Return response as JSON
    return HttpResponse(json.dumps(resp), content_type="application/json")


def view_sub_category(request, pk=None):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'view_sub_category'
    context['page_title'] = 'View Sub Category'

    # Check if a primary key (ID) is provided
    if pk is None:
        # If no ID is provided, set sub-category context to an empty dictionary
        context['sub_category'] = {}
    else:
        # If an ID is provided, retrieve the sub-category with the given ID
        context['sub_category'] = models.SubCategory.objects.get(id=pk)

    # Render the view sub-category page with the context data
    return render(request, 'view_sub_category.html', context)


def manage_sub_category(request, pk=None):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'manage_sub_category'
    context['page_title'] = 'Manage Sub Category'

    # Check if a primary key (ID) is provided
    if pk is None:
        # If no ID is provided, set sub-category context to an empty dictionary
        context['sub_category'] = {}
    else:
        # If an ID is provided, retrieve the sub-category with the given ID
        context['sub_category'] = models.SubCategory.objects.get(id=pk)

    # Retrieve all active categories for selection in the form
    context['categories'] = models.Category.objects.filter(delete_flag=0, status=1).all()

    # Render the manage sub-category page with the context data
    return render(request, 'manage_sub_category.html', context)


def delete_sub_category(request, pk=None):
    # Initialize response dictionary with default values
    resp = {'status': 'failed', 'msg': ''}

    # Check if a valid sub-category ID is provided
    if pk is None:
        resp['msg'] = 'Sub Category ID is invalid'
    else:
        try:
            # Mark the sub-category as deleted by setting the delete_flag to 1
            models.SubCategory.objects.filter(pk=pk).update(delete_flag=1)
            # If successful, display a success message
            messages.success(request, "Sub Category has been deleted successfully.")
            # Update the response status to 'success'
            resp['status'] = 'success'
        except:
            # If an error occurs, set the error message
            resp['msg'] = "Deleting Sub Category Failed"

    # Return response as JSON
    return HttpResponse(json.dumps(resp), content_type="application/json")


def books(request):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'book'
    context['page_title'] = "Book List"

    # Get all active books
    context['books'] = models.Books.objects.filter(delete_flag=0).all()

    # Render the books list page with the context data
    return render(request, 'books.html', context)


@login_required
def save_book(request):
    # Initialize response dictionary with default values
    resp = {'status': 'failed', 'msg': ''}

    # Check if the request method is POST
    if request.method == 'POST':
        # Print POST and FILES data for debugging
        print(request.POST)
        print(request.FILES)

        post = request.POST
        files = request.FILES

        # Check if updating an existing book or creating a new one
        if not post.get('id'):
            form = forms.SaveBook(post, files)
        else:
            book = models.Books.objects.get(id=post['id'])
            form = forms.SaveBook(post, files, instance=book)

        # Validate the form
        if form.is_valid():
            form.save()
            if not post.get('id'):
                messages.success(request, "Book has been saved successfully.")
            else:
                messages.success(request, "Book has been updated successfully.")
            resp['status'] = 'success'
        else:
            # Set error message with form errors
            resp['msg'] = form.errors.as_json()
    else:
        # Set error message if request method is not POST
        resp['msg'] = "There's no data sent with the request"

    # Return response as JSON
    return HttpResponse(json.dumps(resp), content_type="application/json")


def view_book(request, pk=None):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'view_book'
    context['page_title'] = 'View Book'

    # Check if a primary key (ID) is provided
    if pk is None:
        # If no ID is provided, set book context to an empty dictionary
        context['book'] = {}
    else:
        # If an ID is provided, retrieve the book with the given ID
        context['book'] = models.Books.objects.get(id=pk)

    # Render the view book page with the context data
    return render(request, 'view_book.html', context)


@login_required
def manage_book(request, pk=None):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'manage_book'
    context['page_title'] = 'Manage Book'

    # Check if a primary key (ID) is provided
    if pk is None:
        # If no ID is provided, set book context to an empty dictionary
        context['book'] = {}
    else:
        # If an ID is provided, retrieve the book with the given ID
        context['book'] = models.Books.objects.get(id=pk)

    # Retrieve all active sub-categories for selection in the form
    context['sub_categories'] = models.SubCategory.objects.filter(delete_flag=0, status=1).all()

    # Render the manage book page with the context data
    return render(request, 'manage_book.html', context)


@login_required
def delete_book(request, pk=None):
    # Initialize response dictionary with default values
    resp = {'status': 'failed', 'msg': ''}

    # Check if a valid book ID is provided
    if pk is None:
        resp['msg'] = 'Book ID is invalid'
    else:
        try:
            # Mark the book as deleted by setting the delete_flag to 1
            models.Books.objects.filter(pk=pk).update(delete_flag=1)
            # If successful, display a success message
            messages.success(request, "Book has been deleted successfully.")
            # Update the response status to 'success'
            resp['status'] = 'success'
        except:
            # If an error occurs, set the error message
            resp['msg'] = "Deleting Book Failed"

    # Return response as JSON
    return HttpResponse(json.dumps(resp), content_type="application/json")


def videos(request):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'video'
    context['page_title'] = "Video List"

    # Get all active videos
    context['videos'] = models.Videos.objects.filter(delete_flag=0).all()

    # Render the videos list page with the context data
    return render(request, 'videos.html', context)


@login_required
def save_video(request):
    # Initialize response dictionary with default values
    resp = {'status': 'failed', 'msg': ''}

    # Check if the request method is POST
    if request.method == 'POST':
        post = request.POST
        files = request.FILES

        # Debug print statements to check received files
        print("Files received:", files)

        # Get video ID from POST data
        video_id = post.get('id', '')

        # Check if updating an existing video or creating a new one
        if video_id:
            video = get_object_or_404(models.Videos, id=video_id)
            form = forms.SaveVideo(request.POST, request.FILES, instance=video)
        else:
            form = forms.SaveVideo(request.POST, request.FILES)

        # Validate the form
        if form.is_valid():
            instance = form.save()

            # Debug print statements to check saved instance and thumbnail URL
            print("Saved video instance:", instance)
            print("Thumbnail URL:", instance.thumbURL)

            # Display success message
            messages.success(request,
                             "Video has been saved successfully." if not video_id else "Video has been updated successfully.")
            resp['status'] = 'success'
        else:
            # Set error message with form errors
            resp['msg'] = form.errors.as_json()
    else:
        # Set error message if request method is not POST
        resp['msg'] = "There's no data sent with the request"

    # Return response as JSON
    return HttpResponse(json.dumps(resp), content_type="application/json")


def view_video(request, pk=None):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'view_video'
    context['page_title'] = 'View Video'

    # Check if a primary key (ID) is provided
    if pk is None:
        # If no ID is provided, set video context to an empty dictionary
        context['video'] = {}
    else:
        # If an ID is provided, retrieve the video with the given ID
        context['video'] = models.Videos.objects.get(id=pk)

    # Render the view video page with the context data
    return render(request, 'view_video.html', context)


@login_required
def manage_video(request, pk=None):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'manage_video'
    context['page_title'] = 'Manage Video'

    # Check if a primary key (ID) is provided
    if pk is None:
        # If no ID is provided, set video context to an empty dictionary
        context['video'] = {}
    else:
        # If an ID is provided, retrieve the video with the given ID
        context['video'] = models.Videos.objects.get(id=pk)

    # Retrieve all active sub-categories for selection in the form
    context['sub_categories'] = models.SubCategory.objects.filter(delete_flag=0, status=1).all()

    # Render the manage video page with the context data
    return render(request, 'manage_video.html', context)


@login_required
def delete_video(request, pk=None):
    # Initialize response dictionary with default values
    resp = {'status': 'failed', 'msg': ''}

    # Check if a valid video ID is provided
    if pk is None:
        resp['msg'] = 'Video ID is invalid'
    else:
        try:
            # Mark the video as deleted by setting the delete_flag to 1
            models.Videos.objects.filter(pk=pk).update(delete_flag=1)
            # If successful, display a success message
            messages.success(request, "Video has been deleted successfully.")
            # Update the response status to 'success'
            resp['status'] = 'success'
        except:
            # If an error occurs, set the error message
            resp['msg'] = "Deleting Video Failed"

    # Return response as JSON
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def students(request):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'student'
    context['page_title'] = "Student List"

    # Get all active students
    context['students'] = models.Students.objects.filter(delete_flag=0).all()

    # Render the students list page with the context data
    return render(request, 'students.html', context)


@login_required
def save_student(request):
    # Initialize response dictionary with default values
    resp = {'status': 'failed', 'msg': ''}

    # Check if the request method is POST
    if request.method == 'POST':
        post = request.POST

        # Check if updating an existing student or creating a new one
        if not post['id'] == '':
            student = models.Students.objects.get(id=post['id'])
            form = forms.SaveStudent(request.POST, instance=student)
        else:
            form = forms.SaveStudent(request.POST)

        # Validate the form
        if form.is_valid():
            form.save()

            # Display success message
            if post['id'] == '':
                messages.success(request, "Student has been saved successfully.")
            else:
                messages.success(request, "Student has been updated successfully.")

            resp['status'] = 'success'
        else:
            # Collect form errors and set them in the response message
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        # Set error message if request method is not POST
        resp['msg'] = "There's no data sent on the request"

    # Return response as JSON
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def view_student(request, pk=None):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'view_student'
    context['page_title'] = 'View Student'

    # Check if a primary key (ID) is provided
    if pk is None:
        # If no ID is provided, set student context to an empty dictionary
        context['student'] = {}
    else:
        # If an ID is provided, retrieve the student with the given ID
        context['student'] = models.Students.objects.get(id=pk)

    # Render the view student page with the context data
    return render(request, 'view_student.html', context)


@login_required
def manage_student(request, pk=None):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'manage_student'
    context['page_title'] = 'Manage Student'

    # Check if a primary key (ID) is provided
    if pk is None:
        # If no ID is provided, set student context to an empty dictionary
        context['student'] = {}
    else:
        # If an ID is provided, retrieve the student with the given ID
        context['student'] = models.Students.objects.get(id=pk)

    # Retrieve all active sub-categories for selection in the form
    context['sub_categories'] = models.SubCategory.objects.filter(delete_flag=0, status=1).all()

    # Render the manage student page with the context data
    return render(request, 'manage_student.html', context)


@login_required
def delete_student(request, pk=None):
    # Initialize response dictionary with default values
    resp = {'status': 'failed', 'msg': ''}

    # Check if a valid student ID is provided
    if pk is None:
        resp['msg'] = 'Student ID is invalid'
    else:
        try:
            # Mark the student as deleted by setting the delete_flag to 1
            models.Students.objects.filter(pk=pk).update(delete_flag=1)

            # If successful, display a success message
            messages.success(request, "Student has been deleted successfully.")

            # Update the response status to 'success'
            resp['status'] = 'success'
        except:
            # If an error occurs, set the error message
            resp['msg'] = "Deleting Student Failed"

    # Return response as JSON
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def borrows(request):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'borrow'
    context['page_title'] = "Borrowing Transaction List"

    # Get all borrowing transactions, ordered by their status
    context['borrows'] = models.Borrow.objects.order_by('status').all()

    # Render the borrowing transactions list page with the context data
    return render(request, 'borrows.html', context)


@login_required
def save_borrow(request):
    # Initialize response dictionary with default values
    resp = {'status': 'failed', 'msg': ''}

    # Check if the request method is POST
    if request.method == 'POST':
        post = request.POST

        # Check if updating an existing borrowing transaction or creating a new one
        if not post['id'] == '':
            borrow = models.Borrow.objects.get(id=post['id'])
            form = forms.SaveBorrow(request.POST, instance=borrow)
        else:
            form = forms.SaveBorrow(request.POST)

        # Validate the form
        if form.is_valid():
            form.save()

            # Display success message
            if post['id'] == '':
                messages.success(request, "Borrowing Transaction has been saved successfully.")
            else:
                messages.success(request, "Borrowing Transaction has been updated successfully.")

            resp['status'] = 'success'
        else:
            # Collect form errors and set them in the response message
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        # Set error message if request method is not POST
        resp['msg'] = "There's no data sent on the request"

    # Return response as JSON
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def view_borrow(request, pk=None):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'view_borrow'
    context['page_title'] = 'View Transaction Details'

    # Check if a primary key (ID) is provided
    if pk is None:
        # If no ID is provided, set borrowing context to an empty dictionary
        context['borrow'] = {}
    else:
        # If an ID is provided, retrieve the borrowing transaction with the given ID
        context['borrow'] = models.Borrow.objects.get(id=pk)

    # Render the view borrowing transaction page with the context data
    return render(request, 'view_borrow.html', context)


@login_required
def manage_borrow(request, pk=None):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'manage_borrow'
    context['page_title'] = 'Manage Transaction Details'

    # Check if a primary key (ID) is provided
    if pk is None:
        # If no ID is provided, set borrowing context to an empty dictionary
        context['borrow'] = {}
    else:
        # If an ID is provided, retrieve the borrowing transaction with the given ID
        context['borrow'] = models.Borrow.objects.get(id=pk)

    # Retrieve all active students and books for selection in the form
    context['students'] = models.Students.objects.filter(delete_flag=0, status=1).all()
    context['books'] = models.Books.objects.filter(delete_flag=0, status=1).all()

    # Render the manage borrowing transaction page with the context data
    return render(request, 'manage_borrow.html', context)


@login_required
def delete_borrow(request, pk=None):
    # Initialize response dictionary with default values
    resp = {'status': 'failed', 'msg': ''}

    # Check if a valid transaction ID is provided
    if pk is None:
        resp['msg'] = 'Transaction ID is invalid'
    else:
        try:
            # Delete the borrowing transaction with the given ID
            models.Borrow.objects.filter(pk=pk).delete()

            # If successful, display a success message
            messages.success(request, "Transaction has been deleted successfully.")

            # Update the response status to 'success'
            resp['status'] = 'success'
        except:
            # If an error occurs, set the error message
            resp['msg'] = "Deleting Transaction Failed"

    # Return response as JSON
    return HttpResponse(json.dumps(resp), content_type="application/json")


def contact(request, pk=None):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'contact'
    context['page_title'] = 'Contact'

    # Check if a primary key (ID) is provided
    if pk is None:
        # If no ID is provided, set inquiry context to an empty dictionary
        context['inquiry'] = {}
    else:
        # If an ID is provided, retrieve the inquiry with the given ID
        context['inquiry'] = models.Inquiry.objects.get(id=pk)

    # Render the contact page with the context data
    return render(request, 'contact.html', context)


def about_lib(request):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'about'
    context['page_title'] = 'About Us'

    # Render the about library page
    return render(request, 'about_library.html', context)


def inquiry(request):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'inquiry'
    context['page_title'] = "Inquiry List"

    # Get all inquiries
    context['inquiry'] = models.Inquiry.objects.all()

    # Render the inquiry list page with the context data
    return render(request, 'inquiry.html', context)


def save_inquiry(request):
    # Initialize response dictionary with default values
    resp = {'status': 'failed', 'msg': ''}

    # Check if the request method is POST
    if request.method == 'POST':
        post = request.POST

        # Check if updating an existing inquiry or creating a new one
        if not post['id'] == '':
            inquiry = models.Inquiry.objects.get(id=post['id'])
            form = forms.SaveInquiry(request.POST, instance=inquiry)
        else:
            form = forms.SaveInquiry(request.POST)

        # Validate the form
        if form.is_valid():
            form.save()

            # Display success message
            if post['id'] == '':
                messages.success(request, "Your Request has been sent successfully.")
            else:
                messages.success(request, "Error Sending Request.")

            resp['status'] = 'success'
        else:
            # Collect form errors and set them in the response message
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str('<br/>')
                    resp['msg'] += str(f'[{field.name}] {error}')
    else:
        # Set error message if request method is not POST
        resp['msg'] = "There's no data sent on the request"

    # Return response as JSON
    return HttpResponse(json.dumps(resp), content_type="application/json")


def view_inquiry(request, pk=None):
    # Initialize context data for the template
    context = context_data(request)
    context['page'] = 'view_inquiry'
    context['page_title'] = 'View Inquiry'

    # Check if a primary key (ID) is provided
    if pk is None:
        # If no ID is provided, set inquiry context to an empty dictionary
        context['inquiry'] = {}
    else:
        # If an ID is provided, retrieve the inquiry with the given ID
        context['inquiry'] = models.Inquiry.objects.get(id=pk)

    # Render the view inquiry page with the context data
    return render(request, 'view_inquiry.html', context)


def delete_inquiry(request, pk=None):
    # Initialize response dictionary with default values
    resp = {'status': 'failed', 'msg': ''}

    # Check if a valid inquiry ID is provided
    if pk is None:
        resp['msg'] = 'Inquiry ID is invalid'
    else:
        try:
            # Mark the inquiry as deleted by setting the delete_flag to 1
            models.Inquiry.objects.filter(pk=pk).update(delete_flag=1)

            # If successful, display a success message
            messages.success(request, "Inquiry has been deleted successfully.")

            # Update the response status to 'success'
            resp['status'] = 'success'
        except:
            # If an error occurs, set the error message
            resp['msg'] = "Deleting Inquiry Failed"

    # Return response as JSON
    return HttpResponse(json.dumps(resp), content_type="application/json")

