# coding: utf-8
import os

import sys
from random import randint

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudlibrary.settings")
    django.setup()

import json

from book.models import SearchTask, Book, BookTag
from spider.douban.api.save_book_from_api import save_book_from_api
from spider.douban.utils.utils import get_book_id_from_url
from spider.public.html_downloader import HtmlDownloader


def get_douban_book_by_id(book_id, use_proxy=True):
    """给出豆瓣书籍的id, 保存到本地数据库, 并返回本地数据库中书籍对象"""
    _book = Book.objects.filter(info__douban_id=book_id).first()
    if _book:
        print("书籍已下载, 返回本地数据库数据:", _book)
        return _book

    book_meta_str = str(HtmlDownloader.download("https://api.douban.com/v2/book/" + str(book_id), use_proxy=use_proxy), encoding="utf-8")
    book_meta_json = json.loads(book_meta_str)
    if book_meta_json is not None and book_meta_json.get("id") is not None:
        return save_book_from_api(book_meta_json)
    else:
        return None


def get_douban_book_by_url(book_url, use_proxy=True):
    """给出豆瓣书籍的url, 保存到本地数据库, 并返回本地数据库中书籍id"""
    book_id = get_book_id_from_url(book_url)
    if book_id is None or len(str(book_id)) == 0:
        return None
    return get_douban_book_by_id(book_id, use_proxy=use_proxy)


def get_book_by_name(name):
    """通过名称搜索图书, 返回Book对象"""
    data = {
        'start': 0,
        'count': 1,
        'q': str(name)
    }
    search_res_str = str(HtmlDownloader.download("https://api.douban.com/v2/book/search", data=data), encoding="utf-8")
    search_res_json = json.loads(search_res_str)
    print(search_res_json)
    try:
        return save_book_from_api(search_res_json.get("books")[0])
    except Exception as e:
        print(e)
        return None


def search_book_by_name(name):
    try:
        _search_task = SearchTask.objects.filter(search_keyword=name, search_type="search-book-api").first()
        if not _search_task:
            _search_task = SearchTask(search_keyword=name, search_type="search-book-api")
            _search_task.save()

        start = _search_task.search_start

        while True:
            data = {
                'start': start,
                'count': 100,
                'q': str(name)
            }
            search_res_str = str(HtmlDownloader.download("https://api.douban.com/v2/book/search", data=data),
                                 encoding="utf-8")
            search_res_json = json.loads(search_res_str)
            total = int(search_res_json.get("total"))
            print("搜索 - ", name," - 得到书籍 ", total, " 本, 从第 ", start, " 开始", "*" * 30)
            for book in search_res_json.get("books"):
                # print("搜索标签得到书籍:", book)
                _book = save_book_from_api(book)
                # print("保存了书籍:", _book)

            start += min(int(data.get("count")), len(search_res_json.get("books")))
            _search_task.search_start = start
            _search_task.total = search_res_json.get("total")
            _search_task.save()

            if start >= total:
                break
    except Exception as e:
        print(e)


def search_all_tag_book():
    tag_count = BookTag.objects.all().count()
    while True:
        try:
            random_tag = BookTag.objects.all()[randint(0, tag_count-1)]
            search_book_by_name(random_tag.name)
        except Exception as e:
            print(e)


def search_tag_by_name(name):
    """
    通过标签名搜索图书并保存
    :param name:
    :return:
    """
    _search_url = "https://api.douban.com/v2/book/search"
    # _search_task = SearchTask.objects.filter(search_type="tag", search_keyword=name).first()
    # if not _search_task:
    _search_task = SearchTask(search_type="tag", search_keyword=name)

    start = _search_task.search_start
    total = _search_task.total

    while start < total:
        data = {
            'tag': name,
            'start': start,
            'count': 100
        }
        search_res_str = str(HtmlDownloader.download(_search_url, data=data), encoding="utf-8")
        search_res_json = json.loads(search_res_str)
        total = int(search_res_json.get("total"))
        print("搜索到书籍 ", total, " 本, 从第 ", start, " 开始", "*" * 30)
        for book in search_res_json.get("books"):
            print("搜索标签得到书籍:", book)
            _book = save_book_from_api(book)
            print("保存了书籍:", _book)

        start += min(int(data.get("count")), len(search_res_json.get("books")))
        _search_task.search_start = start
        _search_task.total = search_res_json.get("total")
        # _search_task.save()


def search_all_tag():
    while True:
        try:
            tag_count = BookTag.objects.all().count()
            random_tag = BookTag.objects.all()[randint(0, tag_count-1)]
            search_tag_by_name(random_tag.name)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    # search_tag_by_name("教材")
    search_all_tag()
    # search_book("教材")
    # print(get_douban_book_by_id(1220562))
    # print(get_book_by_name("围城"))
    pass
