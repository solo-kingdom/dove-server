# coding: utf-8
import random
import re
import os

import sys
import threading
import traceback
import urllib.parse

sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")

from spider.douban.api.douban_api import get_douban_book_by_url, search_book_by_name

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudlibrary.settings")
    django.setup()

import json

from book.models import SearchTask
from bs4 import BeautifulSoup

from spider.public.html_downloader import HtmlDownloader


hot_tags = []


def get_hot_tags():
    """获取热门标签"""
    tags = []
    url = "https://book.douban.com/tag/?view=cloud"
    soup = BeautifulSoup(HtmlDownloader.download(url, use_proxy=False), 'html.parser')
    links = soup.find_all("a", href=re.compile(r'^/tag/'))
    for link in links:
        tags.append(link.string)
    return tags


def get_book_urls(soup):
    res = []
    try:
        lis = soup.find("div", id="content").find("ul", class_="subject-list").find_all("li")
        for li in lis:
            li_a = li.find("a", href=re.compile(r"douban.com/subject/\d+/"))
            res.append(li_a.get("href"))
    except Exception as e:
        print(e)
        traceback.print_exc()
    return res


def search_tag(search_task):
    search_url = "https://book.douban.com/tag/" + search_task.search_keyword
    # search_url = "https://book.douban.com/tag/" + urllib.parse.quote(search_task.search_keyword)
    while True:
        data = {
            'start': search_task.search_start,
            'type': 'T'
        }
        # print(search_url)
        # print(data)

        soup = BeautifulSoup(HtmlDownloader.download(search_url, data=data, use_proxy=False, delay=0), 'html.parser')
        book_urls = get_book_urls(soup)
        for book_url in book_urls:
            try:
                book = get_douban_book_by_url(book_url)
                print("保存书籍:", book)
            except Exception as e:
                print(e)
                traceback.print_exc()
        search_task.search_start += len(book_urls)
        search_task.save()

        if len(book_urls) == 0:
            break
    return


def solve():
    try:
        hot_tag = random.choice(hot_tags)
        _search_task = SearchTask.objects.filter(search_keyword=hot_tag, search_type="tag-page").first()
        if not _search_task:
            _search_task = SearchTask(search_keyword=hot_tag, search_type="tag-page")
            _search_task.save()

        search_tag(_search_task)
    except Exception as e:
        print(e)


def search_tag_api(_search_task):
    pass


def solve_api():
    try:
        if len(hot_tags) == 0:
            return
        hot_tag = random.choice(hot_tags)
        search_book_by_name(hot_tag)
        # _search_task = SearchTask.objects.filter(search_keyword=hot_tag, search_type="tag-page-api").first()
        # if not _search_task:
        #     _search_task = SearchTask(search_keyword=hot_tag, search_type="tag-page-api")
        #     _search_task.save()
        #
        # search_tag_api(_search_task)
    except Exception as e:
        print(e)


def multi_search_task():
    task_threads = []
    for i in range(10):
        task_threads.append(threading.Thread(target=solve_api))
    for task_thread in task_threads:
        task_thread.setDaemon(True)
        task_thread.start()
    task_threads[-1].join()
    print("OVER")


if __name__ == "__main__":
    # print(get_hot_tags())
    hot_tags = get_hot_tags()
    multi_search_task()
    pass
