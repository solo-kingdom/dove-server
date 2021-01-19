# coding: utf-8
import re
import os

import sys
import traceback
import urllib.parse

import time

from spider.douban.api.douban_api import get_douban_book_by_url
from spider.douban.api.save_book_from_api import get_download_pic

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudlibrary.settings")
    django.setup()

from book.models import Book

for book in Book.objects.all():
    local_pic_url = book.pic
    if len(local_pic_url.split("/")[-1]) == 0:
        try:
            print(book.name, ":", local_pic_url)
            local_pic_url = get_download_pic(book.info.pic_url)
            book.pic = local_pic_url
            book.save()
            # time.sleep(3)
            print("下载了图片:", local_pic_url.split("/")[-1], "\t",book.name)
        except Exception as e:
            print(e)

    # get_download_pic
