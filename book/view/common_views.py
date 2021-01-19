# coding: utf-8
# File: user_views.py
# Author: szhkai@qq.com
from django.shortcuts import render


def return_404_page(request, *args, **kwargs):
    return render(request, '404page.html')

