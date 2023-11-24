from django import forms
from .models import Products, Options


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude = ('user', 'like_users',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Options
        fields = ('content',)