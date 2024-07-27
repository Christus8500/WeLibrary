from django.contrib import admin
from lmsApp import models

# Register your models here.
# Register the Category model with the Django admin.
admin.site.register(models.Category)

# Register the SubCategory model with the Django admin.
admin.site.register(models.SubCategory)

# Register the Books model with the Django admin.
admin.site.register(models.Books)

# Register the Videos model with the Django admin.
admin.site.register(models.Videos)

# Register the Students model with the Django admin.
admin.site.register(models.Students)

# Register the Borrow model with the Django admin.
admin.site.register(models.Borrow)

# Register the Inquiry model with the Django admin.
admin.site.register(models.Inquiry)

