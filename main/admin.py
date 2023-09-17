from django.contrib import admin
from .models import Post , Comment, Share
# Register your models here.
admin.site.name="Arab Social"
admin.site.site_header="Arab Social developed by Mohamed Ahmed"
admin.site.site_title="Arab Social Network"

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Share)
