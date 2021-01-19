# coding: utf-8
import traceback

from bs4 import BeautifulSoup

from spider.public.html_downloader import HtmlDownloader
from spider.public.utils import get_search_book_url
from spider.urllib.book_parser import parse_book_detail
from spider.urllib.save_book import save_book


def search_book(keyword, craw_all=False, download_delay=None):
    try:
        # 获取搜索书籍url
        _url = get_search_book_url(keyword)
        # 下载
        _html_content = HtmlDownloader.download(_url, delay=download_delay)
        _soup = BeautifulSoup(_html_content, 'html.parser')
        # 获取搜索列表
        _search_res = _soup.find(class_='result-list').find_all(class_='result')

        _book_urls = []
        # 获取书籍链接
        if craw_all:
            # 获取搜索到的所有书的 url
            for _t_res in _search_res:
                _t_book_url = _t_res.find('h3').find('a').get('href')
                _book_urls.append(_t_book_url)
        else:
            # 获取搜索到的第一本书的 url
            if len(_search_res) > 0:
                _t_book_url = _search_res[0].find('h3').find('a').get('href')
                _book_urls.append(_t_book_url)

        # 处理书籍 url 列表
        _res = []
        for _book_url in _book_urls:
            try:
                _book_meta = parse_book_detail(_book_url)
                _t_book = save_book(_book_meta)
                _res.append(_t_book)
            except:
                traceback.print_exc()
        return _res
    except:
        traceback.print_exc()
    return None


def craw_tag(keyword):
    pass


if __name__ == "__main__":
    search_res = search_book('围城')
    print(search_res)
    if search_res is not None:
        for _t_search_res in search_res:
            print(_t_search_res.id)

    # search_book('围城', craw_all=True)
