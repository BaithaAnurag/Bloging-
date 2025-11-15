# mainapp/forms.py
from django import forms
from .models import Comment  # make sure you have a Comment model

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'text': forms.Textarea(attrs={'placeholder': 'Write a comment...', 'rows':4}),
        }
