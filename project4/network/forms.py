from django import forms
from django.forms import ModelForm
from .models import Post, Comment
from django.contrib.auth.models import User

class PostForm(ModelForm):
    content = forms.CharField(label='',
                               widget=forms.Textarea(attrs={
                                   'placeholder': '--Write a Post (max 256 characters) --',
                                   'class': 'post-form-input',
                                   'id': 'post-content'
                               }))
    class Meta:
        model = Post
        fields = ['content']

class CommentForm(ModelForm):
    comment = forms.CharField(label='',
                              widget=forms.Textarea)
    
    class Meta:
        model = Comment
        fields = ['comment']
