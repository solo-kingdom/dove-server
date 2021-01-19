# -*- coding: utf-8 -*-
import os
import datetime
import shutil

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
# 从设置中获取图片存取位置
from .settings import IMAGES_STORE

# 使用 Django 模型实现数据存储
import sys

# 如果没有设置 DJANGO_SETTINGS_MODULE, 则设置
if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudlibrary.settings")
    django.setup()

from book.models import Book, BookInformationSource, BookAuthor, BookTag, BookScore, ScrapyTask


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanBookPipeline(object):
    def process_item(self, item, spider):
        # 保存信息到数据库
        # 来源信息
        # 如果数据库中不存在该URL
        if not Book.objects.filter(sources__url=item.get("url")).exists():
            # 书籍信息
            douban_book = Book(name=item.get("name"),
                               source_name=item.get("source_name"),
                               press=item.get("press"),
                               date=item.get("date"),
                               ISBN=item.get("ISBN"),
                               summary=item.get("summary"),
                               pages=item.get("pages"),
                               pic=item.get("image_paths"),
                               pic_url=item.get("image_urls"),
                               )
            douban_book.save()

            book_score = BookScore(score=item.get("scores"),
                                   people_count=item.get("comment_people_count"),
                                   score_rate_five=item.get("score_rate_five"),
                                   score_rate_four=item.get("score_rate_four"),
                                   score_rate_three=item.get("score_rate_three"),
                                   score_rate_two=item.get("score_rate_two"),
                                   score_rate_one=item.get("score_rate_one"),
                                   )
            book_score.save()
            douban_book.scores.add(book_score)

            info_source = BookInformationSource(url=item.get("url"), name="Douban")
            info_source.save()
            douban_book.sources.add(info_source)

            # 标签
            book_tags = []
            origin_tags = item.get("tags")
            for _origin_tag in origin_tags:
                # 先从数据库中取标签
                _t_book_tag = BookTag.objects.filter(name=_origin_tag)
                if not _t_book_tag:
                    _t_book_tag = BookTag(name=_origin_tag)
                    _t_book_tag.save()
                else:
                    _t_book_tag = _t_book_tag[0]
                book_tags.append(_t_book_tag)
                douban_book.tags.add(_t_book_tag)

            # 作者
            book_authors = []
            origin_authors = item.get("author")
            for _origin_author in origin_authors:
                # 先从数据库中获取
                _t_author = BookAuthor.objects.filter(name=_origin_author)
                if not _t_author:
                    _t_author = BookAuthor(name=_origin_author)
                    _t_author.save()
                else:
                    _t_author = _t_author[0]
                book_authors.append(_t_author)
                douban_book.author.add(_t_author)

            # 保存scrapy task
            scrapy_task = ScrapyTask(key=item.get("scrapy_task_key"), obj_id=douban_book.id)
            scrapy_task.save()
        else:
            douban_book = Book.objects.get(sources__url=item.get("url"))
            # 保存scrapy task
            scrapy_task = ScrapyTask(key=item.get("scrapy_task_key"), obj_id=douban_book.id)
            scrapy_task.save()
        return item


class MyImgPipeline(ImagesPipeline):
    """
    图片下载
    """

    # headers = {
    #     'authority': 'img3.doubanio.com',
    #     'method': 'GET',
    #     "path": "",
    #     "scheme": "https",
    #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    #     "accept-encoding": "gzip, deflate, sdch, br",
    #     "accept-language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,nl;q=0.2,es;q=0.2",
    #     "if-modified-since": "Wed, 21 Jan 2004 19:51:30 GMT",
    #     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #                   'Chrome/55.0.2883.87 Safari/537.36',
    # }

    def get_media_requests(self, item, info):
        _image_urls = item.get('image_urls')
        # print('=' * 100, _image_urls)
        # 如果存在 image_urls
        if _image_urls:
            # 如果是列表
            if isinstance(_image_urls, list):
                for _image_url in _image_urls:
                    # _headers = self.get_headers(_image_url, item.get("url"))
                    yield Request(_image_url)
            # 如果是字符串
            elif isinstance(_image_urls, str):
                # _headers = self.get_headers(_image_urls, item.get("url"))
                yield Request(_image_urls)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        _date_now = datetime.datetime.now()
        _year = str(_date_now.year)
        _mouth = str(_date_now.month)
        _day = str(_date_now.day)
        if not image_paths:
            raise DropItem("Item contains no images")

        # 将图片移动到按日期编排的目录下
        _after_path = []
        for _image_path in image_paths:
            _before_path = os.path.join(IMAGES_STORE, _image_path)
            _new_path_dir = os.path.join(IMAGES_STORE, _year, _mouth, _day)
            _new_path_dir_with_full = os.path.join(IMAGES_STORE, _year, _mouth, _day, 'full')
            _new_path = os.path.join(_new_path_dir, _image_path)
            # print('*' * 50,'\n',  _before_path, '\n',_new_path, '\n', _new_path_dir)

            # 移动图片
            if not os.path.exists(_new_path_dir_with_full):
                os.makedirs(_new_path_dir_with_full)
            if os.path.exists(_before_path):
                shutil.move(_before_path, _new_path)

            # 添加新的图片路径
            _after_path.append(os.path.join(_year, _mouth, _day, _image_path))

        # 更新item中图片路径
        # print("下载图片完成:", _after_path)
        item['image_paths'] = os.path.join("/media/book/img/", _after_path[0]) if len(_after_path) > 0  else None
        return item

        # def get_headers(self, image_url, subject_url):
        #     _headers = self.headers
        #     _headers[":path"] = urllib.parse.urlparse(image_url).path
        #     _headers["referer"] = subject_url
        #     return _headers
