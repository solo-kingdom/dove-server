#!/usr/bin python3
# coding: utf-8

"""
FILE: generate_book_keyword.py
DATE: 17-6-22 下午3:29
DESC: 生成书籍关键词
"""
import os
import sys

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudlibrary.settings")
    django.setup()

import jieba
import jieba.analyse

from book.models import Book, BookKeyword

TOP_K = 30  # 获取前 k 个关键词
punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')


def get_top_n_with_weight(content):
    return jieba.analyse.extract_tags(content, topK=TOP_K, withWeight=True)


def generate_keyword_v2():
    print("generate_keyword_v2")
    with open('keywords.txt', 'w') as f:
        for book in Book.objects.all():
            res_str = str(book.id)
            keywords = {}
            key_str = ""
            key_str += book.name
            key_str += book.summary
            filter_punct = ''.join(filter(lambda x: x not in punct, key_str))
            for item in get_top_n_with_weight(filter_punct):
                keywords[item[0]] = item[1]

            # 整合标签
            max_count = 1
            for tag_ship in book.booktagship_set.all():
                max_count = max(max_count, tag_ship.count)
            for tag_ship in book.booktagship_set.all():
                # print(tag_ship)
                _tag_name = tag_ship.tag.name
                if keywords.get(_tag_name):
                    keywords[_tag_name] *= tag_ship.count / max_count
                else:
                    keywords[_tag_name] = tag_ship.count / max_count
            for key, value in keywords.items():
                res_str += ' ' + key + ' ' + str(value)
            # print(res_str)
            res_str += '\n'
            f.write(res_str)


def generate_keyword_v1():
    for book in Book.objects.all():
        print(book.id, " - ", book.name)
        # 保存最终的结果
        keywords = {}
        # 对简介精确分词, 获取 top n 及频率
        summary_keywords = get_top_n_with_weight(book.summary)
        # 整合到 keywords dict
        for keyword in summary_keywords:
            # print(keyword[0], " - ", keyword[1])
            keywords[keyword[0]] = keyword[1]

        # 对书名精确分词, 获得关键词 list; 如果简介中也存在该关键词则增加相应比重
        for keyword in jieba.cut(book.name):
            if keywords.get(keyword):
                keywords[keyword] *= 1.5
            else:
                # 如果简介中不存该关键词, 保存到keywords
                keywords[keyword] = 1

        # 整合标签
        max_count = 1
        for tag_ship in book.booktagship_set.all():
            max_count = max(max_count, tag_ship.count)
        for tag_ship in book.booktagship_set.all():
            # print(tag_ship)
            _tag_name = tag_ship.tag.name
            if keywords.get(_tag_name):
                keywords[_tag_name] *= tag_ship.count / max_count
            else:
                keywords[_tag_name] = tag_ship.count / max_count

        # 保存到数据库
        print(keywords)
        book.keywords.clear()
        for key, value in keywords.items():
            book_keyword = BookKeyword(name=key, weight=value)
            book_keyword.save()
            book.keywords.add(book_keyword)


if __name__ == "__main__":
    generate_keyword_v1()
    # s = "我来到。北：京:--C++sd大学"
    # filter_str = ''.join(filter(lambda x: x not in punct, s))
    # print(filter_str)
    # print([i for i in jieba.cut(filter_str)])
    pass
