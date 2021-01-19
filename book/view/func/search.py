# coding: utf-8
from book.models import Book, BookList


def solve_search_book(keyword):
    books = Book.objects.filter(name__contains=keyword)
    return books


def solve_search_booklist(keyword):
    booklist = BookList.objects.filter(name__contains=keyword)
    return booklist
