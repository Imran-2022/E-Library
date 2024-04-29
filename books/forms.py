from django import forms
from .models import Books

class PostForm(forms.ModelForm):
    class Meta:
        model=Books
        # fields= '__all__'
        # fields=['name','bio']
        # exclude=['bio']
        exclude=['author']
