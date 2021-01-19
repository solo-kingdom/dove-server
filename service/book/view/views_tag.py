# coding: utf-8
from django.shortcuts import render
from el_pagination.decorators import page_template

from book.models import Book, BookList, BookTag


@page_template('module/_booklist_list.html')
def tag_booklist(request, tag_id=None, template='tag-page.html', extra_context=None):
    booktag = BookTag.objects.filter(id=tag_id).first()
    context = {
        'title': '标签',
        'list': BookList.objects.filter(tags__in=[booktag]),
        'tag': booktag,
        'type': 'booklist'
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context=context)


@page_template('module/_book_list.html')
def tag_book(request, tag_id=None, template='tag-page.html', extra_context=None):
    booktag = BookTag.objects.filter(id=tag_id).first()
    context = {
        'title': '标签',
        'list': Book.objects.filter(tags__in=[booktag]),
        'tag': booktag,
        'type': 'book'
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context=context)


def hot_tag_collection(request):
    """热门标签集合"""
    context = {
        'title': '热门标签',
    }
    return render(request, 'hot_tag_collection.html', context=context)
