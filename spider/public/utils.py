# coding=utf-8
import datetime
import os
import random
import re
import string
import urllib
import urllib.parse


def convert_to_int(int_str, default=None):
    try:
        num = re.findall(r'\d*\.?\d*', int_str)[0]
        # int_str = re.sub(r'\s', '', int_str)
        if len(re.findall(r'[kK千]', int_str)) > 0:
            res = int(float(num) * 1000)
        elif len(re.findall(r'[wW万]', int_str)) > 0:
            res = int(float(num) * 10000)
        else:
            res = int(num)
        pass
    except:
        res = default
        pass
    return res


def get_pic_save_path():
    # 获取年月日
    _date_now = datetime.datetime.now()
    _year = str(_date_now.year)
    _mouth = str(_date_now.month)
    _day = str(_date_now.day)
    return os.path.join('media', 'book', 'img', _year, _mouth, _day)


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


def generate_random_str_id(length=32):
    return ''.join(random.sample(string.ascii_letters+string.digits, length))


def get_tag_url(tag_name):
    _url = "https://book.douban.com/tag/" + str(tag_name)
    return _url


def write_to_file(file_name, content):
    with open(file_name, 'wb') as fo:
        fo.write(content)

if __name__ == '__main__':
    print(generate_random_str_id())
    print(generate_random_str_id(10))
    print(generate_random_str_id(20))
    print(get_pic_url_path())
    # print(convert_to_int('1.4万'))
    # print(convert_to_int('1.4w'))
    # print(convert_to_int('1.4K'))
    # print(convert_to_int('1213 123'))
    # print(convert_to_int('.3w'))
    # print(convert_to_int('1213 123'))
    pass
