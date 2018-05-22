from django import forms
from .models import MobileModel

class MobileForm(forms.Form):
    class Meta:
        model = MobileModel
        fields = ('title', 'image', 'contend',)