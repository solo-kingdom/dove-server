# coding: utf-8
from django.http import Http404
from django.shortcuts import render

from book.models import Book


def book_detail(request, book_id):
    """
    书籍详情
    :param request:
    :param book_id:
    :return:
    """
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return render(request, '404page.html')
    context = {
        'title': '书云 - 详情 - ' + book.name,
        'bookid': book_id,
        'book': book,
    }
    return render(request, 'book-detail.html', context=context)

