from urllib.request import Request
from django.contrib import admin

# Register your models here.
from .models import Profile ,RequestFriend

admin.site.register(Profile)
admin.site.register(RequestFriend)