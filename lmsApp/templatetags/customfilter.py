from atexit import register
from django import template
from cryptography.fernet import Fernet
from django.conf import settings
import os
import re

# Creating an instance of template.Library to register custom template filters.
register = template.Library()


# Defining a custom filter to replace occurrences of a specified string with a blank string.
@register.filter
def replaceBlank(value, stringVal=""):
    # Convert the value to a string and replace occurrences of stringVal with an empty string.
    value = str(value).replace(stringVal, '')
    return value


# Defining a custom filter to encrypt a given value using Fernet encryption.
@register.filter
def encryptdata(value):
    # Create a Fernet object using the encryption key from Django settings.
    fernet = Fernet(settings.ID_ENCRYPTION_KEY)
    # Encrypt the value after converting it to bytes.
    value = fernet.encrypt(str(value).encode())
    return value


# Defining a custom filter to extract the original filename from a given path.
@register.filter
def original_filename(value):
    """
    Extracts the original filename from the given path.
    Removes any appended random strings by assuming the
    original filename is before the first underscore in the base filename.
    """
    if not value:
        return ''

    # Get the base filename from the given path.
    filename = os.path.basename(value)

    # Use regex to find and remove the appended random string pattern.
    original_name = re.sub(r'(_[a-zA-Z0-9]{6,}\.)', '.', filename)

    return original_name
