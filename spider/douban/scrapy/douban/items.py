# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
# import sys
# sys.path.append("..")
# sys.path.append("../..")

import scrapy


class DoubanBookItem(scrapy.Item):
    """
    豆瓣图书 item
    """
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 书名
    name = scrapy.Field()
    # 原作名
    source_name = scrapy.Field()
    # 出版社
    press = scrapy.Field()
    # 出版日期
    date = scrapy.Field()
    # 页数
    pages = scrapy.Field()
    # ISBN
    ISBN = scrapy.Field()
    # 书的作者
    author = scrapy.Field()
    # 译者
    translator = scrapy.Field()
    # 标签
    tags = scrapy.Field()
    # 简介
    summary = scrapy.Field()
    # 信息来源
    sources = scrapy.Field()
    # 评分
    scores = scrapy.Field()
    # 评分人数
    comment_people_count = scrapy.Field()
    # x星评分
    score_rate_five = scrapy.Field()
    score_rate_four = scrapy.Field()
    score_rate_three = scrapy.Field()
    score_rate_two = scrapy.Field()
    score_rate_one = scrapy.Field()
    # 图片
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
    # 丛书
    series_name = scrapy.Field()
    # 丛书地址
    series_url = scrapy.Field()
    # 定价
    price = scrapy.Field()
    # 书籍链接
    url = scrapy.Field()
    # scrapy task
    scrapy_task_key = scrapy.Field()


def get_bookitem_attr_name(_name):
    """根据中文提示获取item字段名"""
    if isinstance(_name, str):
        _name = _name.strip()
        if _name.find("出版社") >= 0:
            return "press"
        elif _name.find("出版年") >= 0:
            return "date"
        elif _name.find("页数") >= 0:
            return "pages"
        elif _name.find("定价") >= 0:
            return "price"
        elif _name.find("ISBN") >= 0:
            return "ISBN"
    return None
