# coding: utf-8
import os
import sys

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudlibrary.settings")
    django.setup()

from book.models import BookList
from django.contrib.auth.models import User
user = User.objects.filter(username='bovenson').first()

print(user.username)

for booklist in BookList.objects.all():
    if not booklist.user or booklist.user.id:
        booklist.user = user
        booklist.save()
