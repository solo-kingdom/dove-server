# coding: utf-8
from django import forms
from django.contrib.auth.models import User

from book.models import BookRemark, BookList


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'nickname']


class BookRemarkForm(forms.ModelForm):
    """书单中书籍评语Form"""
    class Meta:
        model = BookRemark
        fields = ['booklist', 'book', 'content']


class BookListForm(forms.ModelForm):
    """书单Form"""
    class Meta:
        model = BookList
        fields = ['name', 'summary']
