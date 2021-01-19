# coding: utf-8
import os

# 如果没有设置 DJANGO_SETTINGS_MODULE, 则设置
import sys
import traceback

from spider.douban.utils.utils import generate_douban_book_url

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudlibrary.settings")
    django.setup()

from book.models import Book, BookScore, BookTag, BookAuthor, BookTagShip, BookInfo, BookSeries
from spider.public.image_downloader import download_pic
from spider.public.utils import get_pic_save_path
from cloudlibrary.settings import BASE_DIR


def save_book_from_api(book_meta):
    """
    保存从豆瓣获取的数据到数据库
    :param book_meta: 豆瓣返回的书籍数据信息
    :return: 新建的Book对象
    """
    _douban_book_id = book_meta.get("id")
    if not _douban_book_id:
        print("豆瓣返回的格式不正确")
        return None

    # 保存信息到数据库
    # 需要新建的对象: Book, BookInfo, BookTag, BookAuthor, BookScore, BookTagShip, BookSeries

    # 如果数据库中不存在该id
    _book = Book.objects.filter(info__douban_id=book_meta.get("id")).first()
    if not _book:
        try:
            # 下载图片
            # 图片保存路径
            _pic_url = book_meta.get('images').get('large')
            _pic_url_full_path = ""
            try:
                _pic_url_full_path = get_download_pic(_pic_url)
            except Exception as e:
                print("下载图片出错:", e)
            # 书籍信息

            # BookInfo
            book_info = None
            try:
                book_info = BookInfo.objects.create(
                    origin_title=book_meta.get("origin_title"),
                    subtitle=book_meta.get("subtitle"),
                    binding=book_meta.get("binding"),
                    catalog=book_meta.get("catalog")[:4990] if book_meta.get("catalog") else "",
                    pages=book_meta.get("pages"),
                    publisher=book_meta.get("publisher"),
                    isbn=book_meta.get("isbn13") if book_meta.get("isbn13") else book_meta.get("isbn10"),
                    url=book_meta.get("alt"),
                    pic_url=book_meta.get("images").get("large"),
                    douban_id=book_meta.get("id"),
                    price=book_meta.get("price"),
                    pubdate=book_meta.get("pubdate")
                )
                book_info.save()

                for translator_name in book_meta.get("translator"):
                    # 先从数据库中获取
                    _translator = BookAuthor.objects.filter(name=translator_name).first()
                    if not _translator:
                        # 如果不存在该作者, 则创建
                        _translator = BookAuthor(name=translator_name)
                        _translator.save()
                    book_info.translator.add(_translator)
            except Exception as e:
                print('保存书籍 - 保存BookInfo时出错:', e)
                traceback.print_exc()

            book_score = None
            # 评分
            try:
                # 新建 BookScore 对象
                book_score = BookScore(score=book_meta.get("rating").get("average"),
                                       people_count=book_meta.get("rating").get("numRaters"),
                                       max=book_meta.get("rating").get("max"),
                                       min=book_meta.get("rating").get("min"))
                book_score.save()
            except Exception as e:
                print('保存书籍 - 保存评分时出错:', e)
                traceback.print_exc()

            # 新建 Book 对象
            douban_book = Book(name=book_meta.get("title"),
                               summary=book_meta.get("summary")[:4990] if book_meta.get("summary") else "",
                               pic=_pic_url_full_path,
                               info=book_info,
                               score=book_score)
            douban_book.save()

            # 标签
            try:
                # 从json数据中抽取标签
                for _tag in book_meta.get("tags"):
                    _tag_name = _tag.get("name")
                    _tag_count = _tag.get("count")
                    # 先从数据库中取标签
                    _t_book_tag = BookTag.objects.filter(name=_tag_name).first()
                    if not _t_book_tag:
                        # 如果没有该标签则新建
                        _t_book_tag = BookTag(name=_tag_name, count=1)
                        _t_book_tag.save()
                    else:
                        _t_book_tag.count += 1
                        _t_book_tag.save()
                    # 新建 BookTagShip 对象
                    book_tag_ship = BookTagShip.objects.create(book=douban_book, tag=_t_book_tag, count=int(_tag_count))
                    book_tag_ship.save()
            except Exception as e:
                print('保存书籍 - 保存标签时出错:', e)
                traceback.print_exc()

            try:
                # 作者
                for _origin_author in book_meta.get("author"):
                    # 先从数据库中获取
                    _t_author = BookAuthor.objects.filter(name=_origin_author).first()
                    _author_intro = book_meta.get("author_intro")[:4990] if book_meta.get("author_intro") else "",
                    _author_intro = str(_author_intro).strip()
                    if not _t_author:
                        # 如果不存在该作者, 则创建
                        _t_author = BookAuthor(name=_origin_author, description=_author_intro)
                        _t_author.save()
                    if len(_t_author.description) == 0 and len(_author_intro) != 0:
                        _t_author.description = _author_intro
                        _t_author.save()
                    douban_book.author.add(_t_author)
            except Exception as e:
                print('保存书籍 - 保存作者时出错:', e)
                traceback.print_exc()

            # BookSeries
            try:
                if book_meta.get("series") and book_meta.get("series").get("id"):
                    book_series = BookSeries.objects.filter(douban_id=book_meta.get("series").get("id")).first()
                    if not book_series:
                        book_series = BookSeries.objects.create(name=book_meta.get("series").get("title"),
                                                                douban_id=book_meta.get("series").get("id"))
                        book_series.save()
                        book_series.books.add(douban_book)
            except Exception as e:
                print('保存书籍 - 保存BookSeries时出错:', e)
                traceback.print_exc()

            return douban_book
        except Exception as e:
            print(e)
            traceback.print_exc()

    else:
        print("书籍已下载, 返回数据库记录.")
        return _book


def get_download_pic(pic_url):
    _pic_relative_path = get_pic_save_path()  # 得到相对路径, 主要是按照下载年月日分在不同文件夹下
    _pic_url_path = '/' + '/'.join(_pic_relative_path.split(os.path.sep))
    _save_path = os.path.join(BASE_DIR, _pic_relative_path)  # 获取图片保存的绝对路径
    _pic_name = download_pic(url=pic_url, save_path=_save_path)  # 图片名称
    _pic_url_full_path = os.path.join(_pic_url_path, _pic_name)
    return _pic_url_full_path
