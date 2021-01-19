# coding: utf-8
import random
import re
import os
import sys

from spider.douban.scrapy.run_spider import craw_book

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


# def craw_book(book_name):
#     try:
#         # print(os.environ.get('SCRAPY_SETTINGS_MODULE'))
#         # print(os.path.abspath(__file__))
#         _key = str(random.random())[2:]
#
#         process = CrawlerProcess(get_project_settings())
#         process.crawl(BookSpider, run_type=BookSpiderRunType.CRAW_BOOK, craw_keyword=book_name, need_login=False, scrapy_task_key=_key)
#         print("1111")
#         print("2222")
#
#         # spider = BookSpider(run_type=BookSpiderRunType.CRAW_BOOK, craw_keyword=book_name, need_login=False, scrapy_task_key=_key)
#         # spider.craw()
#         # process.crawl(BookSpider, run_type=BookSpiderRunType.CRAW_BOOK, craw_keyword=book_name, need_login=False, scrapy_task_key=_key)
#         # process.start()
#         # process.stop()
#
#         # runner = CrawlerRunner(get_project_settings())
#         #
#         # running_crawler = runner.crawl(BookSpider, run_type=BookSpiderRunType.CRAW_BOOK, craw_keyword=book_name,
#         #                                 need_login=False, scrapy_task_key=_key)
#         # running_crawler.addBoth(lambda _: reactor.stop())
#         # reactor.run()
#
#         _scrapy_task = ScrapyTask.objects.get(key=_key)
#         return _scrapy_task.obj_id
#     except:
#         # import traceback
#         # traceback.print_exc()
#         return None


def import_from_xlsx(xlsx_file):
    _booklists = []
    workbook = load_workbook(xlsx_file)
    sheet_names = workbook.get_sheet_names()
    for sheet_name in sheet_names:
        _booklist = ImportBookListStructure()
        worksheet = workbook.get_sheet_by_name(sheet_name)
        rows = worksheet.rows
        for row in rows:
            _booklist.name = row[0].value
            _booklist.books = [str(col.value).strip() for col in row[1:]
                               if col.value is not None and len(str(col.value).strip()) > 0]
            _booklists.append(_booklist)
    return _booklists


def write_to_db(_booklists):
    for _booklist in _booklists:
        _has_book = False
        _booklist_model = BookList(name=_booklist.name)
        for _book in _booklist.books:
            try:
                _book = re.sub(r'[《》]+', '', str(_book))
                _book_id = craw_book(_book)
                print('book name:', _book, ' id:', _book_id)
                if _book_id is not None:
                    _book_model = Book.objects.get(id=_book_id)
                    _has_book = True
                    _booklist_model.books.add(_book_model)
            except:
                pass
        if _has_book:
            _booklist_model.save()


def start(file_name):
    booklists = []
    if is_specific_suffix(file_name, 'xlsx'):
        booklists = import_from_xlsx(file_name)
    else:
        print('Unsupported file format')
        exit(1)

    write_to_db(booklists)


if __name__ == '__main__':
    start('booklist_test.xlsx')
