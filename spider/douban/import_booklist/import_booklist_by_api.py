# coding: utf-8
import os
import re
import sys

# 设置环境变量, 从命令行运行脚本
import traceback

import time
from scrapy.spidermiddlewares.httperror import HttpError

from spider.douban.api.douban_api import get_book_by_name

sys.path.append('..')
sys.path.append('../..')

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudlibrary.settings")
    django.setup()

from book.models import BookList, Book
from common.util.utils import is_specific_suffix
from openpyxl import load_workbook


class ImportBookListStructure(object):
    name = ""
    summary = ""
    books = []


def import_from_xlsx(xlsx_file):
    """
    从xlsx文件中读取书单
    :param xlsx_file: 
    :return: 
    """
    _booklists = []
    workbook = load_workbook(xlsx_file)
    sheet_names = workbook.get_sheet_names()
    for sheet_name in sheet_names:
        worksheet = workbook.get_sheet_by_name(sheet_name)
        rows = worksheet.rows
        for row in rows:
            _booklist = ImportBookListStructure()
            _booklist.name = row[0].value
            _booklist.books = [str(col.value).strip() for col in row[1:]
                               if col.value is not None and len(str(col.value).strip()) > 0]
            # _booklists.append(_booklist)
            _booklists.insert(0, _booklist)
    return _booklists


def write_to_db(_booklists):
    """
    写入数据库
    :param _booklists: 
    :return: 
    """
    for _booklist in _booklists:
        # 书单中是否有图书
        _has_book = False

        # 新建书单对象
        _booklist_model = BookList.objects.filter(name=_booklist.name).first()
        if not _booklist_model:
            _booklist_model = BookList(name=_booklist.name)
            _booklist_model.save()
        # 便利书单中图书
        for _book_name in _booklist.books:
            try:
                print("获取书籍:", _book_name)
                # 获取书籍名称
                _book_name = re.sub(r'[《》]+', '', str(_book_name))
                # 获取搜索结果
                _book = Book.objects.filter(name=_book_name).first()
                if not _book:
                    print("下载书籍:", _book_name)
                    _book = get_book_by_name(_book_name)
                else:
                    print("本地数据库中有该书籍:" + _book_name)
                if _book:
                    _booklist_model.books.add(_book)
            except Exception as e:
                traceback.print_exc()
                print(e)
        if _has_book:
            if len(_booklist_model.books.all()) == 0:
                _booklist_model.delete()
            else:
                print('保存书单')
                _booklist_model.save()


def start(file_name):
    booklists = []
    if is_specific_suffix(file_name, 'xlsx'):
        booklists = import_from_xlsx(file_name)
    else:
        print('不支持的文件格式')
        exit(1)

    write_to_db(booklists)


if __name__ == '__main__':
    start('booklist.xlsx')
