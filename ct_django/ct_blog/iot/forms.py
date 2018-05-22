from django import forms
from .models import Comment, Post
class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author',None)
        self.post = kwargs.pop('post',None)
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = Comment
        fields = ["body"]

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'img', 'contend',)
    '''
    def __init__(self, author, *args, **kwargs):
        self.author = author
        super(PostForm, self).__init__(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        self.instance.author = self.author
        super(PostForm, self).save(*args, **kwargs)
    '''
