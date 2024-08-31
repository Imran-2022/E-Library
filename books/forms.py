from django import forms
from .models import Books
from .models import Comment

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        
class PostForm(forms.ModelForm):
    class Meta:
        model=Books
        # fields= '__all__'
        # fields=['name','bio']
        # exclude=['bio']
        exclude=['author']
