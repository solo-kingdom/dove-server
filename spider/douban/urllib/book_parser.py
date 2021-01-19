# coding: utf-8
import re
import traceback

from bs4 import BeautifulSoup
from bs4 import Tag

from common.log.log import MyLogger
from spider.public.html_downloader import HtmlDownloader

my_logger = MyLogger()


def parse_book_detail(root_url):
    """
    提取豆瓣书籍详情并返回元数据
    :param root_url: 
    :return: 书籍元数据
    """
    # 提取数据
    response = HtmlDownloader.download_response(root_url)
    soup = BeautifulSoup(response.read(), "html.parser")
    info = soup.find(id='info')
    if info:
        # 如果找到书籍信息
        _book_item = {'url': str(response.url)}

        # 提取名称
        try:
            _book_item['name'] = str(soup.find(id='wrapper').find('h1').find('span').string)
        except:
            traceback.print_exc()
            pass

        items = info.find_all('span')
        for item in items:
            if not item or not item.string:
                continue
            _key = str(item.string).strip()
            if _key.startswith("丛书"):
                # 如果是丛书, 特殊处理
                _a_element = item.find_next('a')
                if _a_element:
                    _book_item['series_name'] = str(_a_element.string).strip()
                    _book_item['series_url'] = str(_a_element.get('href')).strip()
            elif _key.startswith("译者"):
                # 如果是译者, 特殊处理
                _element = item.find_next_sibling('a')
                _translator = []
                while _element and _element.name != 'span':
                    if isinstance(_element, Tag) and _element.name == 'a':
                        if _element.string:
                            _name = replace_mul_space(str(_element.string).strip())
                            _translator.append(_name)
                    _element = _element.find_next_sibling()
                    _book_item['translator'] = _translator
            elif _key.startswith("作者"):
                # 如果是作者, 特殊处理
                _element = item.find_next_sibling('a')
                _authors = []
                if _element:
                    while _element and _element.name != 'span':
                        if isinstance(_element, Tag) and _element.name == 'a':
                            if _element.string:
                                _name = replace_mul_space(str(_element.string).strip())
                                _authors.append(_name)
                        _element = _element.find_next_sibling()
                    _book_item['author'] = _authors
            else:
                _value = str(item.find_next_sibling(text=True)).strip()

                _attr_name = get_bookitem_attr_name(_key)
                if _attr_name is not None:
                    _book_item[_attr_name] = _value
                else:
                    my_logger.warning("BookItem缺少字段: " + _key)

        # 获取书籍图片
        _pic_soup = soup.find(id='mainpic')
        if _pic_soup:
            _img_element = _pic_soup.find_next('img')
            _book_item['image_urls'] = str(_img_element.get('src')).strip()

        # 评分
        _scores_info_soup = soup.find(id='interest_sectl')
        if _scores_info_soup:
            try:
                _book_item['scores'] = str(_scores_info_soup.find('strong', class_=re.compile('rating_num')).string).strip()
            except Exception as e:
                my_logger.error("解析书籍分数时出错")
            try:
                _book_item['comment_people_count'] = str(_scores_info_soup.find('span', property='v:votes').string).strip()
            except:
                my_logger.error("解析评论人数时出错")
                traceback.print_exc()
            _score_stars = _scores_info_soup.find_all('span', class_='rating_per')
            if len(_score_stars) == 5:
                _book_item['score_rate_five'] = str(_score_stars[0].string).strip()
                _book_item['score_rate_four'] = str(_score_stars[1].string).strip()
                _book_item['score_rate_three'] = str(_score_stars[2].string).strip()
                _book_item['score_rate_two'] = str(_score_stars[3].string).strip()
                _book_item['score_rate_one'] = str(_score_stars[4].string).strip()

        # 获取简介
        _intro_soup = soup.find(id='link-report')
        if _intro_soup:
            _intro_div = _intro_soup.find('div', class_='intro')
            if _intro_div:
                _intro_p = _intro_div.find('p')
                if _intro_p:
                    _book_item['summary'] = str(_intro_p.string).strip()

        # 获取标签
        _tag_soup = soup.find(id='db-tags-section')
        if _tag_soup:
            _tag_div = _tag_soup.find('div', class_='indent')
            if _tag_div:
                _tags = _tag_soup.find_all('a')
                _tag_list = []
                for _tag in _tags:
                    _tag_list.append(str(_tag.string).strip())
                _book_item['tags'] = _tag_list

        return _book_item


def replace_mul_space(s):
    # 将多个连续空白符替换为一个空格符
    return re.sub(r'\s+', ' ', s)


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
