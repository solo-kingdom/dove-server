#!/usr/bin python3
# coding: utf-8

"""
FILE: get_hot_tags.py
DATE: 17-7-10 下午3:40
DESC: 
"""
import os
import sys
from bs4 import BeautifulSoup

from spider.public.html_downloader import HtmlDownloader

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

from book.models import BookTag, HotTagCollection


def solve():
    """获取热门标签"""
    tags = []
    url = "https://book.douban.com/tag/"
    soup = BeautifulSoup(HtmlDownloader.download(url, use_proxy=False), 'html.parser')
    # links = soup.find_all("a", href=re.compile(r'^/tag/'))
    collections = soup.find_all('a', class_='tag-title-wrapper')
    HotTagCollection.objects.all().delete()
    for collection in collections:
        collection_name = collection['name']
        new_collection = HotTagCollection(title=collection_name)
        new_collection.save()
        for item in collection.find_next_sibling('table').find_all('a'):
            tag_name = item.string
            tag = BookTag.objects.filter(name=tag_name).first()
            if not tag:
                tag = BookTag(name=tag_name)
            new_collection.tags.add(tag)


solve()
