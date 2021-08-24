from django.contrib import admin
from .models import Comment, Profile, City, Post

# Register your models here.
admin.site.register(Profile)
admin.site.register(City)
admin.site.register(Post)
admin.site.register(Comment)
