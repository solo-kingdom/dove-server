#!/usr/bin python3
# coding: utf-8

"""
FILE: search_all_tag_book.py
DATE: 17-6-26 上午10:11
DESC: 
"""
import os
import sys
import threading
from random import choice

sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")


if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudlibrary.settings")
    django.setup()


from spider.douban.api.douban_api import search_all_tag_book


def search_tag_book_task():
    task_threads = []
    for i in range(10):
        task_threads.append(threading.Thread(target=search_all_tag_book))
    for task_thread in task_threads:
        task_thread.setDaemon(True)
        task_thread.start()
    task_threads[-1].join()
    print("OVER")


if __name__ == "__main__":
    search_tag_book_task()
    pass
