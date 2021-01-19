# coding: utf-8
import os
import sys

import time

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudlibrary.settings")
    django.setup()
from book.models import Book, BookList

# books = Book.objects.all()
# for book in books:
#     book.delete()

# booklist = BookList.objects.all().first()
# print(booklist.tags)


# for booklist in BookList.objects.all():
#     print(booklist.name)
#     booklist.save()
#     print(booklist.tags)

while True:
    print(Book.objects.all().count())
    time.sleep(60)
