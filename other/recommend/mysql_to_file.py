#!/usr/bin python3
# coding: utf-8

"""
FILE: mysql_to_file.py
DATE: 17-7-10 下午4:52
DESC: 
"""
import os
import re
import sys
from time import sleep

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudlibrary.settings")
    django.setup()

from book.models import Book


def save_book_info_to_file(file_path='.'):
    """保存数据库中书籍数据到文件"""
    def save_summary():
        summary_file = os.path.join(file_path, 'book_summary.txt')
        with open(summary_file, 'w') as f:
            for book in Book.objects.all():
                # print()
                f.write(str(book.id) + "|" + re.sub(r'\s', '', book.summary) + "\n")
    # 保存简介
    save_summary()

save_book_info_to_file('/home/public/data/cloudlibrary')
