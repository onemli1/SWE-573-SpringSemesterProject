from django import forms
from blog.models import BlogPost, Space, Comment

class CreateBlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'category', 'space', 'post_type')

class CreateSpaceForm(forms.ModelForm):

    class Meta:
        model = Space
        fields = ('name', 'category')


class UpdateBlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ('title', 'body', 'category', 'space', 'post_type')
    
    def save(self, commit=True):
        blog_post = self.instance
        blog_post.title = self.cleaned_data['title']
        blog_post.body = self.cleaned_data['body']

        if commit:
            blog_post.save()
        
        return blog_post


class CreateCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)


















