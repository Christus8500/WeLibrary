from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
      # Home page
      path('', views.home, name="home-page"),
      # Login page
      path('login', views.login_page, name='login-page'),
      # User registration page
      path('register', views.userregister, name='register-page'),
      # Save user registration
      path('save_register', views.save_register, name='register-user'),
      # User login
      path('user_login', views.login_user, name='login-user'),
      # Home page
      path('home', views.home, name='home-page'),
      # Contact page
      path('contact', views.contact, name='contact-page'),
      # Logout
      path('logout', views.logout_user, name='logout'),
      # User profile page
      path('profile', views.profile, name='profile-page'),
      # Update user password
      path('update_password', views.update_password, name='update-password'),
      # Update user profile
      path('update_profile', views.update_profile, name='update-profile'),
      # About us page
      path('about_us', views.about_lib, name='about-page'),

      # User management
      path('users', views.users, name='user-page'),
      path('manage_user', views.manage_user, name='manage-user'),
      path('manage_user/<int:pk>', views.manage_user, name='manage-user-pk'),
      path('save_user', views.save_user, name='save-user'),
      path('delete_user/<int:pk>', views.delete_user, name='delete-user'),

      # Category management
      path('category', views.category, name='category-page'),
      path('manage_category', views.manage_category, name='manage-category'),
      path('manage_category/<int:pk>', views.manage_category, name='manage-category-pk'),
      path('view_category/<int:pk>', views.view_category, name='view-category-pk'),
      path('save_category', views.save_category, name='save-category'),
      path('delete_category/<int:pk>', views.delete_category, name='delete-category'),

      # Sub-category management
      path('sub_category', views.sub_category, name='sub_category-page'),
      path('manage_sub_category', views.manage_sub_category, name='manage-sub_category'),
      path('manage_sub_category/<int:pk>', views.manage_sub_category, name='manage-sub_category-pk'),
      path('view_sub_category/<int:pk>', views.view_sub_category, name='view-sub_category-pk'),
      path('save_sub_category', views.save_sub_category, name='save-sub_category'),
      path('delete_sub_category/<int:pk>', views.delete_sub_category, name='delete-sub_category'),

      # Book management
      path('books', views.books, name='book-page'),
      path('manage_book', views.manage_book, name='manage-book'),
      path('manage_book/<int:pk>', views.manage_book, name='manage-book-pk'),
      path('view_book/<int:pk>', views.view_book, name='view-book-pk'),
      path('save_book', views.save_book, name='save-book'),
      path('delete_book/<int:pk>', views.delete_book, name='delete-book'),

      # Video management
      path('videos', views.videos, name='video-page'),
      path('manage_video', views.manage_video, name='manage-video'),
      path('manage_video/<int:pk>', views.manage_video, name='manage-video-pk'),
      path('view_video/<int:pk>', views.view_video, name='view-video-pk'),
      path('save_video', views.save_video, name='save-video'),
      path('delete_video/<int:pk>', views.delete_video, name='delete-video'),

      # Student management
      path('students', views.students, name='student-page'),
      path('manage_student', views.manage_student, name='manage-student'),
      path('manage_student/<int:pk>', views.manage_student, name='manage-student-pk'),
      path('view_student/<int:pk>', views.view_student, name='view-student-pk'),
      path('save_student', views.save_student, name='save-student'),
      path('delete_student/<int:pk>', views.delete_student, name='delete-student'),

      # Borrowing transactions management
      path('borrows', views.borrows, name='borrow-page'),
      path('manage_borrow', views.manage_borrow, name='manage-borrow'),
      path('manage_borrow/<int:pk>', views.manage_borrow, name='manage-borrow-pk'),
      path('view_borrow/<int:pk>', views.view_borrow, name='view-borrow-pk'),
      path('save_borrow', views.save_borrow, name='save-borrow'),
      path('delete_borrow/<int:pk>', views.delete_borrow, name='delete-borrow'),

      # Inquiry management
      path('inquiry', views.inquiry, name='inquiry-page'),
      path('view_inquiry/<int:pk>', views.view_inquiry, name='view-inquiry-pk'),
      path('save_inquiry', views.save_inquiry, name='save-inquiry'),
      path('delete_inquiry/<int:pk>', views.delete_inquiry, name='delete-inquiry'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
