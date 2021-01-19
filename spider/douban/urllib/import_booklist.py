# coding: utf-8
import random
import re
import os
import sys

# 设置环境变量, 从命令行运行脚本
sys.path.append('..')
sys.path.append('../..')

from spider.douban.urllib.book_spider import search_book

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudlibrary.settings")
    django.setup()

from book.models import BookList
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
            _booklists.append(_booklist)
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

        # 导入的时候, 如果同名书单存在, 则不导入
        if BookList.objects.filter(name=_booklist.name).exists():
            print('书单:', _booklist.name , ' 已经存在, 将不会被再次导入')
            continue

        # 新建书单对象
        _booklist_model = BookList(name=_booklist.name)
        _booklist_model.save()
        # 便利书单中图书
        for _book_name in _booklist.books:
            try:
                # 获取书籍名称
                _book_name = re.sub(r'[《》]+', '', str(_book_name))
                # 获取搜索结果, 设置两秒下载延迟
                _book_list = search_book(_book_name, download_delay=2)
                print(_book_list)
                # 如果有搜索结果
                if len(_book_list) > 0:
                    _has_book = True
                    for _book in _book_list:
                        print('添加了书籍:', _book.id)
                        _booklist_model.books.add(_book)
            except:
                pass
        if _has_book:
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
    # start('booklist_test.xlsx')
