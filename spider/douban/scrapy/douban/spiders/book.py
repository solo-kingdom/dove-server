# coding: utf-8
import random
import urllib.parse
import sys
import traceback
from configparser import ConfigParser
from enum import Enum

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request, FormRequest

from book.db.db_operation import is_book_url_exists
from common.log.log import MyLogger

sys.path.append('..')
sys.path.append('../..')

from spider.douban.douban.spiders.book_parse import parse_book_detail

my_logger = MyLogger()


class BookSpiderRunType(Enum):
    """
    # 爬取类型
    # CRAW_BOOK: 根据书名,只爬取搜索到的第一条记录
    # CRAW_BOOK_ALL: 根据书名,只爬取搜索到的多条
    # CRAW_TAG: 爬取跟定的标签名
    """
    OTHER = 0
    CRAW_BOOK = 1
    CRAW_BOOK_ALL = 2
    CRAW_TAG = 3


class BookSpider(scrapy.Spider):

    # 指定爬取类型的,爬取关键词
    run_type = BookSpiderRunType.OTHER
    craw_keyword = ''

    name = "book"
    complete_page_urls = set()
    need_login = True
    scrapy_task_key = ''

    def __init__(self, domain='', *args, **kwargs):
        super(BookSpider, self).__init__(*args, **kwargs)
        _run_type = kwargs.get('run_type')
        _craw_keyword = kwargs.get('craw_keyword')
        if isinstance(_run_type, BookSpiderRunType):
            self.run_type = _run_type
            self.craw_keyword = _craw_keyword
            if kwargs.get('need_login') is not None:
                self.need_login = kwargs.get('need_login')
            self.scrapy_task_key = kwargs.get('scrapy_task_key')
        else:
            print('给定爬取类型不正确.')
            return

    login_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,nl;q=0.2,es;q=0.2",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "accounts.douban.com",
        "Origin": "https://accounts.douban.com",
        "Referer": "https://accounts.douban.com/login",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/55.0.2883.87 Safari/537.36"
    }

    def start_requests(self):
        # 判断需不需要登录
        if self.need_login:
            return [Request("https://accounts.douban.com/login",
                            meta={'cookiejar': 1},
                            headers=self.login_headers,
                            callback=self.post_login)]
        else:
            return [Request("https://www.douban.com/", callback=self.after_login)]

    def post_login(self, response):
        try:
            print("登陆豆瓣")

            # 读取账号密码
            cf = ConfigParser()
            cf.read("douban_account.ini")
            username = cf.get("account", "username")
            password = cf.get("account", "password")

            formdata = {
                "source": "None",
                "redir": "https://www.douban.com/",
                "form_email": str(username),
                "form_password": str(password),
                "login": "登录"
            }
            return [FormRequest.from_response(response=response,
                                              meta={'cookiejar': response.meta['cookiejar']},
                                              headers=self.login_headers,
                                              formdata=formdata,
                                              callback=self.after_login,
                                              dont_filter=True)]
        except Exception as e:
            print(e)
            print("读取账号文件失败, 尝试直接抓取.")
            return [Request("https://www.douban.com", callback=self.after_login)]

    # def start_requests(self, response=None):
    def after_login(self, response=None):
        if self.need_login:
            if response is not None and str(response.url).find("login") >= 0:
                print("LOG: 登陆失败, request.url - ", response.url)
            print("LOG: After Login url - ", response.url)

        if self.run_type == BookSpiderRunType.CRAW_BOOK:
            # 爬取搜索的第一个结果
            self.logger.info("爬取搜索:" + self.craw_keyword)
            _url = get_search_book_url(self.craw_keyword)
            yield scrapy.Request(url=_url, callback=self.parse_search_page)
        elif self.run_type == BookSpiderRunType.CRAW_BOOK_ALL:
            # 爬取搜索的多个结果
            self.logger.info("爬取搜索:" + self.craw_keyword)
            _url = get_search_book_url(self.craw_keyword)
            yield scrapy.Request(url=_url, callback=self.parse_search_page_all)
        elif self.run_type == BookSpiderRunType.CRAW_TAG:
            # 爬取标签
            self.logger.info("爬取标签:" + self.craw_keyword)
            _url = get_tag_url(self.craw_keyword)
            self.logger.info("url: " + _url)
            yield scrapy.Request(url=_url, callback=self.parse_tag_page)

        # 提取参数
        # print(sys.argv)
        # for _argv in sys.argv:
        #     _argv_split = str(_argv).split("=", 1)
        #     if len(_argv_split) > 1:
        #         if _argv_split[0] == "book_name":
        #             self.logger.info("爬取搜索:" + _argv_split[1])
        #             _url = get_search_book_url(_argv_split[1])
        #             yield scrapy.Request(url=_url, callback=self.parse_search_page)
        #         elif _argv_split[0] == "book_name_all":
        #             self.logger.info("爬取搜索:" + _argv_split[1])
        #             _url = get_search_book_url(_argv_split[1])
        #             yield scrapy.Request(url=_url, callback=self.parse_search_page_all)
        #         elif _argv_split[0] == "tag":
        #             self.logger.info("爬取标签:" + _argv_split[1])
        #             _url = get_tag_url(_argv_split[1])
        #             self.logger.info("url: " + _url)
        #             yield scrapy.Request(url=_url, callback=self.parse_tag_page)

    def parse(self, response):
        pass

    def parse_search_page(self, response):
        """
        处理搜索结果
        :param response: Scrapy Response 对象
        :return:
        """
        try:
            _soup = BeautifulSoup(response.body, 'html.parser')
            _search_res = _soup.find(class_='result-list').find(class_='result')
            # 获取搜索到的第一本书的 url
            _t_book_url = _search_res.find('h3').find('a').get('href')
            yield scrapy.Request(url=_t_book_url, callback=self.parse_detail)
        except Exception as e:
            # traceback.print_exc()
            self.logger.error("爬取", response.url, "时出错:", e)

    def parse_search_page_all(self, response):
        """
        处理搜索结果
        :param response: Scrapy Response 对象
        :return:
        """
        try:
            _soup = BeautifulSoup(response.body, 'html.parser')
            _search_res = _soup.find(class_='result-list').find_all(class_='result')
            # 获取搜索到的所有书的 url
            for _t_res in _search_res:
                _t_book_url = _t_res.find('h3').find('a').get('href')
                yield scrapy.Request(url=_t_book_url, callback=self.parse_detail)
        except Exception as e:
            # traceback.print_exc()
            self.logger.error("爬取", response.url, "时出错:", e)

    def parse_tag_page(self, response):
        """
        处理某个标签内数据
        :param response: Scrapy Response 对象
        :return:
        """
        try:
            # 如果当前页面已经爬取, 跳过
            if str(response.url) in self.complete_page_urls:
                return
            # 添加当前页面到 complete_page_urls
            self.complete_page_urls.add(str(response.url))

            # 解析图书记录
            _soup = BeautifulSoup(response.body, 'html.parser')
            _book_list_div = _soup.find(id='subject_list')
            if _book_list_div:
                # 如果找到图书列表div, 则处理图书列表
                _book_list = _book_list_div.find('ul', class_='subject-list').find_all('li')
                for _book_item in _book_list:
                    _book_a = _book_item.find('div', class_='pic').find('a')
                    _book_url = _book_a.get('href')
                    # 爬去书籍详情
                    # 判断 如果数据库中没有记录再爬取
                    if not is_book_url_exists(_book_url):
                        yield scrapy.Request(url=_book_url, callback=self.parse_detail)

            # 解析标签页页码
            _pages = _soup.find('div', class_='paginator')
            if _pages:
                _pages_a = _pages.find_all('a')
                for _page_a in _pages_a:
                    _page_href = response.urljoin(_page_a.get('href'))
                    # print("*" * 50, _page_href)
                    if _page_href not in self.complete_page_urls:
                        # 如果complete_page_urls中没有_page_href,则爬取
                        yield scrapy.Request(url=_page_href, callback=self.parse_tag_page)
        except Exception as e:
            my_logger.error("爬取" + response.url + "时出错:" + str(e))
            my_logger.error(traceback.print_exc())
            traceback.print_exc()
            self.logger.error("爬取", response.url, "时出错:", e)

    def parse_detail(self, response):
        """
        解析图书详情页
        :param response: Scrapy Response 对象
        :return: DoubanBookItem对象
        """
        try:
            _book_item = parse_book_detail(response)
            # print('_book_item type:', type(_book_item))
            # print(_book_item)
            # if isinstance(_book_item, dict):
            _book_item['scrapy_task_key'] = self.scrapy_task_key
            yield _book_item
        except Exception as e:
            traceback.print_exc()
            self.logger.error("爬取", response.url, "时出错:", e)
            pass


def get_search_book_url(book_name):
    """
    生成检索url
    urlcat固定为1001, 豆瓣中表明搜索的是图书
    :param book_name: 书名
    :return:
    """
    _params = urllib.parse.urlencode({'cat': 1001, 'q': book_name})
    _url = "https://www.douban.com/search?%s" % _params
    return _url


def get_tag_url(tag_name):
    _url = "https://book.douban.com/tag/" + str(tag_name)
    return _url


def write_to_file(file_name, content):
    with open(file_name, 'wb') as fo:
        fo.write(content)


if __name__ == "__main__":
    print(get_search_book_url("简爱"))
    pass
