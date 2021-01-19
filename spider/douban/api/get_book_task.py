#!/usr/bin python3
# coding: utf-8

"""
FILE: get_book_task.py
DATE: 17-6-21 下午4:28
DESC: 
"""
import sys
import threading

sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")

from spider.douban.api.douban_api import search_all_tag, search_book_by_name


def search_tag_task():
    task_threads = []
    for i in range(10):
        task_threads.append(threading.Thread(target=search_all_tag))
    for task_thread in task_threads:
        task_thread.setDaemon(True)
        task_thread.start()
    task_threads[-1].join()
    print("OVER")


if __name__ == "__main__":
    search_tag_task()
    pass
    # search_tag_by_name("教材")
#    search_all_tag()
