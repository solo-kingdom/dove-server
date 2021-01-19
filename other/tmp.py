# coding: utf-8
import random
import re
import os
import sys

# 设置环境变量, 从命令行运行脚本
# sys.path.append('..')
# sys.path.append('../..')
#
# if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
#     import django
#
#     pathname = os.path.dirname(os.path.abspath(__file__))
#     sys.path.insert(0, pathname)
#     sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../')))
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudlibrary.settings")
#     django.setup()
#
# from book.models import BookList
#
# for booklist in BookList.objects.all():
#     if len(booklist.books.all()) == 0:
#         booklist.delete()
#
# for i in range(1, 10): print(i)


# s = "https://book.douban.com/subject/27031874/?icn=index-editionrecommend/458154564515/"
# print(re.search(r'/(\d+)/', s).group())
# print(re.search(r'/(\d+)/', s).group(1))
import jieba

punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')

print([i for i in jieba.cut("我来到。北：京:--C+sd大学")])
