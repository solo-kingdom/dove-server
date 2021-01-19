# coding: utf-8
import re


def get_book_id_from_url(_url):
    if isinstance(_url, str) and _url.find("douban.com") > 0:
        _res = re.search(r'subject/(\d+)/', _url)
        if _res is not None:
            return _res.group(1)
    return None


def generate_douban_book_url(book_id):
    return "https://book.douban.com/subject/%s/" % str(book_id)


if __name__ == "__main__":
    print(generate_douban_book_url(100))
