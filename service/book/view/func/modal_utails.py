# coding: utf-8
from django.db.models import QuerySet

from book.models import BookAuthor, BookTag


def trance_authors_to_list(authors):
    """转化author的queryset为list对象"""

    if isinstance(authors, QuerySet):
        _res = []
        for author in authors:
            if isinstance(author, BookAuthor):
                _res.append({
                    'name': author.name
                })
        return _res
    return []


def trance_tags_to_list(tags):
    """转化tag的queryset为list对象"""

    if isinstance(tags, QuerySet):
        _res = []
        for tag in tags:
            if isinstance(tag, BookTag):
                _res.append({
                    'name': tag.name
                })
        return _res
    return []
