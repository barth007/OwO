from django import forms
from . models import Blog_Comment

class NewCommentForm(forms.ModelForm):

    class Meta:
        model = Blog_Comment
        fields = ['content']
