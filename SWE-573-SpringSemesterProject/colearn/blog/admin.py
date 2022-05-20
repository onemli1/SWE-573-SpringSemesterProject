from django.contrib import admin

from blog.models import BlogPost, Comment, Notification

admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Notification)
