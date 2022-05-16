from django.contrib import admin

from blog.models import BlogPost, Category, Space, Comment, Notification

admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(Space)
admin.site.register(Comment)
admin.site.register(Notification)
