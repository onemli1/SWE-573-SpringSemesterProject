from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings

from ckeditor.fields import RichTextField

BLOG_TYPES = [('Article','Article'), ('Question', 'Question'), ('Video', 'Video'), ('Lecture Note', 'Lecture Note')]


class Category(models.Model):
    name                    = models.CharField(max_length=35, unique=True)

    def __str__(self):
        return self.name
    

class Space(models.Model):
    name                    = models.CharField(max_length=30, unique=True)
    category                = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    


class BlogPost(models.Model):
    title                   = models.CharField(max_length=50, null=False, blank=False)
    body                    = RichTextField(blank=True, null=True)
    category                = models.ForeignKey(Category, on_delete=models.CASCADE)
    space                   = models.ForeignKey(Space, on_delete=models.CASCADE)
    post_type               = models.CharField(max_length=30, choices=BLOG_TYPES)
    date_published          = models.DateTimeField(auto_now_add=True, verbose_name='date published')
    date_updated            = models.DateTimeField(auto_now=True, verbose_name='date updated')
    author                  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug                    = models.SlugField(blank=True, unique=True)
    likes                   = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes_post', blank=True, null=True)
    unlikes                 = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='unlikes_post', blank=True, null=True)

    def total_likes(self):
        return self.likes.count()
    
    def total_unlikes(self):
        return self.unlikes.count()

    def __str__(self):
        return self.title


def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)


class Comment(models.Model):
    post                    = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    author                  = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment_author', on_delete=models.CASCADE)
    body                    = models.TextField()
    date_added              = models.DateTimeField(auto_now_add=True)
    likes                   = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes_comment', blank=True)
    unlikes                 = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='unlikes_comment', blank=True)


    def total_likes(self):
        return self.likes.count()
    
    def total_unlikes(self):
        return self.unlikes.count()

    def __str__(self):
        return f"{self.post.title} - {self.author.username}"
    

class Notification(models.Model):
    ## 1-Like 2-Comment
    notification_type       = models.SmallIntegerField()
    to_user                 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user               = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post                    = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    comment                 = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="+", blank=True, null=True)
    date                    = models.DateTimeField(default=timezone.now)
    user_has_seen           = models.BooleanField(default=False)
    


















