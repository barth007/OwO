from django import forms
from . models import Blog, Blog_Comment

class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'content', 'image', 'slug']

class NewCommentForm(forms.ModelForm):

    class Meta:
        model = Blog_Comment
        fields = ['content']