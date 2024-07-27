from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from PIL import Image
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager


# Create your models here.
class Category(models.Model):
    # Define fields for the Category model
    name = models.CharField(max_length=250)  # Name of the category
    description = models.TextField(blank=True, null=True)  # Description of the category, optional
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default=1)  # Status of the category, either Active or Inactive
    delete_flag = models.IntegerField(default=0)  # Flag to indicate if the category is marked for deletion
    date_added = models.DateTimeField(default=timezone.now)  # Date when the category was added
    date_created = models.DateTimeField(auto_now=True)  # Date when the category was last modified

    class Meta:
        verbose_name_plural = "List of Categories"  # Plural name for the model in admin interface

    def __str__(self):
        # String representation of the Category object
        return str(f"{self.name}")  # Return the name of the category as the string representation


class SubCategory(models.Model):
    # ForeignKey relationship with Category model, on deletion of parent category, delete subcategory
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)  # Name of the subcategory
    description = models.TextField(blank=True, null=True)  # Description of the subcategory, optional
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default=1)  # Status of the subcategory, either Active or Inactive
    delete_flag = models.IntegerField(default=0)  # Flag to indicate if the subcategory is marked for deletion
    date_added = models.DateTimeField(default=timezone.now)  # Date when the subcategory was added
    date_created = models.DateTimeField(auto_now=True)  # Date when the subcategory was last modified

    class Meta:
        verbose_name_plural = "List of Categories"  # Plural name for the model in admin interface

    def __str__(self):
        # String representation of the SubCategory object
        return str(f"{self.category} - {self.name}")  # Return the category and name of the subcategory as the string representation


class Books(models.Model):
    # ForeignKey relationship with SubCategory model, on deletion of parent subcategory, delete book
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=250)  # ISBN number of the book
    title = models.CharField(max_length=250)  # Title of the book
    description = models.TextField(blank=True, null=True)  # Description of the book, optional
    author = models.TextField(blank=True, null=True)  # Author of the book, optional
    publisher = models.CharField(max_length=250)  # Publisher of the book
    date_published = models.DateTimeField()  # Date when the book was published
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default=1)  # Status of the book, either Active or Inactive
    file = models.FileField(upload_to='books/', null=True)  # File field to upload the book file
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)  # Image field for the cover of the book, optional
    download = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default=1, null=True)  # Download status of the book
    delete_flag = models.IntegerField(default=0)  # Flag to indicate if the book is marked for deletion
    date_added = models.DateTimeField(default=timezone.now)  # Date when the book was added
    date_created = models.DateTimeField(auto_now=True)  # Date when the book was last modified

    class Meta:
        verbose_name_plural = "List of Books"  # Plural name for the model in admin interface

    @property
    def fileURL(self):
        # Get the URL of the uploaded book file
        try:
            url = self.file.url
        except:
            url = ''
        return url

    @property
    def imageURL(self):
        # Get the URL of the cover image of the book
        try:
            url = self.cover_image.url
        except:
            url = ''
        return url

    def __str__(self):
        # String representation of the Books object
        return str(f"{self.isbn} - {self.title}")  # Return the ISBN and title of the book as the string representation


class Videos(models.Model):
    # ForeignKey relationship with SubCategory model, on deletion of parent subcategory, delete video
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)  # Title of the video
    description = models.TextField(blank=True, null=True)  # Description of the video, optional
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default='1')  # Status of the video, either Active or Inactive
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)  # File field to upload the video file
    thumbnail_image = models.ImageField(upload_to='video_thumbnails/', null=True, blank=True)  # Image field for the thumbnail of the video, optional
    download = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default='1', null=True)  # Download status of the video
    delete_flag = models.IntegerField(default=0)  # Flag to indicate if the video is marked for deletion
    date_added = models.DateTimeField(default=timezone.now)  # Date when the video was added
    date_created = models.DateTimeField(auto_now=True)  # Date when the video was last modified

    class Meta:
        verbose_name_plural = "List of Videos"  # Plural name for the model in admin interface

    @property
    def fileURL(self):
        # Get the URL of the uploaded video file
        try:
            return self.video_file.url
        except ValueError:
            return ''

    @property
    def thumbURL(self):
        # Get the URL of the thumbnail image of the video
        try:
            return self.thumbnail_image.url
        except ValueError:
            return ''

    def __str__(self):
        # String representation of the Videos object
        return f"{self.title} - {self.date_added}"  # Return the title and date added of the video as the string representation


class Students(models.Model):
    code = models.CharField(max_length=250)  # Code for the student
    first_name = models.CharField(max_length=250)  # First name of the student
    middle_name = models.CharField(max_length=250, blank=True, null=True)  # Middle name of the student, optional
    last_name = models.CharField(max_length=250)  # Last name of the student
    gender = models.CharField(max_length=20, choices=(('Male', 'Male'), ('Female', 'Female')), default='Male')  # Gender of the student
    contact = models.CharField(max_length=250)  # Contact number of the student
    email = models.CharField(max_length=250)  # Email address of the student
    address = models.CharField(max_length=250)  # Address of the student
    department = models.CharField(max_length=250, blank=True, null=True)  # Department of the student, optional
    course = models.CharField(max_length=250, blank=True, null=True)  # Course of the student, optional
    status = models.CharField(max_length=2, choices=(('1', 'Active'), ('2', 'Inactive')), default=1)  # Status of the student, either Active or Inactive
    delete_flag = models.IntegerField(default=0)  # Flag to indicate if the student is marked for deletion
    date_added = models.DateTimeField(default=timezone.now)  # Date when the student was added
    date_created = models.DateTimeField(auto_now=True)  # Date when the student was last modified

    class Meta:
        verbose_name_plural = "List of Students"  # Plural name for the model in admin interface

    def __str__(self):
        # String representation of the Students object
        # Check if middle name exists, if yes, include it in the string representation
        return str(
            f"{self.code} - {self.first_name}{' ' + self.middle_name if not self.middle_name == '' else ''} {self.last_name}")

    def name(self):
        # Get the full name of the student
        # Check if middle name exists, if yes, include it in the full name
        return str(f"{self.first_name}{' ' + self.middle_name if not self.middle_name == '' else ''} {self.last_name}")


class Borrow(models.Model):
    # ForeignKey relationship with Students model, on deletion of parent student, delete borrowing transaction
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name="student_id_fk")
    # ForeignKey relationship with Books model, on deletion of parent book, delete borrowing transaction
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="book_id_fk")
    borrowing_date = models.DateField()  # Date when the book is borrowed
    return_date = models.DateField()  # Date when the book is expected to be returned
    status = models.CharField(max_length=2, choices=(('1', 'Pending'), ('2', 'Returned')), default=1)  # Status of the borrowing transaction, either Pending or Returned
    date_added = models.DateTimeField(default=timezone.now)  # Date when the borrowing transaction was added
    date_created = models.DateTimeField(auto_now=True)  # Date when the borrowing transaction was last modified

    class Meta:
        verbose_name_plural = "Borrowing Transactions"  # Plural name for the model in admin interface

    def __str__(self):
        # String representation of the Borrow object
        return str(f"{self.student.code}")  # Return the student code as the string representation


class Inquiry(models.Model):
    name = models.CharField(max_length=250)  # Name of the person making the inquiry
    email = models.CharField(max_length=250)  # Email address of the person making the inquiry
    topic = models.CharField(max_length=250)  # Topic of the inquiry
    message = models.TextField(blank=True, null=True)  # Message of the inquiry, optional
    date_created = models.DateTimeField(auto_now=True)  # Date when the inquiry was created

    class Meta:
        verbose_name_plural = "List of Inquiries"  # Plural name for the model in admin interface

    def __str__(self):
        # String representation of the Inquiry object
        return str(f"{self.name} - {self.topic}")  # Return the name and topic of the inquiry as the string representation

