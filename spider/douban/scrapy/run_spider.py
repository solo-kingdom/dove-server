# coding: utf-8
import os
import sys
import random

sys.path.append('..')
sys.path.append('../..')
sys.path.append('../../..')

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spider.douban.douban.spiders.book import BookSpider, BookSpiderRunType
from book.models import ScrapyTask
import threading


def craw_book_thread(book_name):
    try:
        # print(os.environ.get('SCRAPY_SETTINGS_MODULE'))
        # print(os.path.abspath(__file__))
        _key = str(random.random())[2:]
        process = CrawlerProcess(get_project_settings())
        process.crawl(BookSpider, run_type=BookSpiderRunType.CRAW_BOOK, craw_keyword=book_name, need_login=False,
                      scrapy_task_key=_key)
        process.start()
        _scrapy_task = ScrapyTask.objects.get(key=_key)
        return _scrapy_task.obj_id
    except:
        import traceback
        traceback.print_exc()
        return None


def craw_book(book_name):
    t = threading.Thread(target=craw_book_thread, args=(book_name,))
    t.start()
    t.join()


if __name__ == '__main__':
    # print(random.random())
    # print(craw_book_thread('假如给我三天光明'))
    # print(craw_book_thread('假如给我三天光明'))
    for i in range(2):
        craw_book('假如给我三天光明')