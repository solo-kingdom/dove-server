# coding: utf-8
import os
import sys

from spider.douban.utils.utils import generate_douban_book_url, get_book_id_from_url

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudlibrary.settings")
    django.setup()

from book.models import BookList, Book
from django.contrib.auth.models import User

for book in Book.objects.all():
    book.douban_id = get_book_id_from_url(book.sources.all().first().url)
    # print(get_book_id_from_url(book.sources.all().first().url))
    book.save()
