from django import forms
from .models import PostModel, Comment

class PostModelForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = [
            'title',
            'img',
            'content'
        ]

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author',None)
        self.post = kwargs.pop('post',None)
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = Comment
        fields = ["body"]