# coding: utf-8
import os

# 如果没有设置 DJANGO_SETTINGS_MODULE, 则设置
import sys

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    import django

    pathname = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, pathname)
    sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudlibrary.settings")
    django.setup()

from book.models import Book, BookScore, BookInformationSource, BookTag, BookAuthor
from spider.public.image_downloader import download_pic
from spider.public.utils import get_pic_save_path
from cloudlibrary.settings import BASE_DIR


def save_book(book_meta):
    print(book_meta)
    # 保存信息到数据库
    # 来源信息
    # 如果数据库中不存在该URL
    if not Book.objects.filter(sources__url=book_meta.get("url")).exists():
        # 下载图片
        # 图片保存路径
        _pic_url = book_meta.get('image_urls')
        # 下载
        _pic_relative_path = get_pic_save_path()
        _pic_url_path = '/' + '/'.join(_pic_relative_path.split(os.path.sep))
        _save_path = os.path.join(BASE_DIR, _pic_relative_path)
        _pic_name = download_pic(url=_pic_url, save_path=_save_path)
        book_meta['image_paths'] = os.path.join(_pic_url_path, _pic_name)

        # 书籍信息
        douban_book = Book(name=book_meta.get("name"),
                           source_name=book_meta.get("source_name"),
                           press=book_meta.get("press"),
                           date=book_meta.get("date"),
                           ISBN=book_meta.get("ISBN"),
                           summary=book_meta.get("summary"),
                           pages=book_meta.get("pages"),
                           pic=book_meta.get("image_paths"),
                           pic_url=book_meta.get("image_urls"),
                           )
        douban_book.save()

        book_score = BookScore(score=book_meta.get("scores"),
                               people_count=book_meta.get("comment_people_count"),
                               score_rate_five=book_meta.get("score_rate_five"),
                               score_rate_four=book_meta.get("score_rate_four"),
                               score_rate_three=book_meta.get("score_rate_three"),
                               score_rate_two=book_meta.get("score_rate_two"),
                               score_rate_one=book_meta.get("score_rate_one"),
                               )
        book_score.save()
        douban_book.scores.add(book_score)

        info_source = BookInformationSource(url=book_meta.get("url"), name="Douban")
        info_source.save()
        douban_book.sources.add(info_source)

        # 标签
        book_tags = []
        origin_tags = book_meta.get("tags")
        for _origin_tag in origin_tags:
            # 先从数据库中取标签
            _t_book_tag = BookTag.objects.filter(name=_origin_tag)
            if not _t_book_tag:
                _t_book_tag = BookTag(name=_origin_tag)
                _t_book_tag.save()
            else:
                _t_book_tag = _t_book_tag[0]
            book_tags.append(_t_book_tag)
            douban_book.tags.add(_t_book_tag)

        # 作者
        book_authors = []
        origin_authors = book_meta.get("author")
        for _origin_author in origin_authors:
            # 先从数据库中获取
            _t_author = BookAuthor.objects.filter(name=_origin_author)
            if not _t_author:
                _t_author = BookAuthor(name=_origin_author)
                _t_author.save()
            else:
                _t_author = _t_author[0]
            book_authors.append(_t_author)
            douban_book.author.add(_t_author)
        return douban_book
    else:
        print("书籍已下载, 返回数据库记录.")
        douban_book = Book.objects.get(sources__url=book_meta.get("url"))
        return douban_book
