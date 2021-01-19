# coding: utf-8
# 如果没有设置 DJANGO_SETTINGS_MODULE, 则设置
import os

import sys

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudlibrary.settings")
    django.setup()

from book.models import Book


def is_book_url_exists(url):
    return Book.objects.filter(sources__url=url).exists()


if __name__ == "__main__":
    print(is_book_url_exists("asdf"))
    print(is_book_url_exists("asdfs"))
