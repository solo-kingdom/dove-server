# coding: utf-8
# 从数据库中获取记录并分页, 返回分页信息字典
from django.core.paginator import Paginator, EmptyPage

from book.models import Book, BookList
from cloudlibrary.settings import INDEX_PAGE_ITEM_COUNT


def get_book_list_page_dict(page=1):
    """
    获取书籍分页信息
    :param page:
    :return:
    """
    return split_to_page(Book.objects.all(), page)


def get_booklist_list_page_dict(page=1):
    """
    获取书单分页信息
    :param page:
    :return:
    """
    return split_to_page(BookList.objects.all(), page)


def split_to_page(items, page):
    # 获取 page, 默认第一页
    try:
        page = int(page)
        if page < 1:
            page = 1
    except:
        page = 1

    # 分页
    # 分页列表
    page_list = Paginator(items, INDEX_PAGE_ITEM_COUNT)
    # 总分页数
    total_page = page_list.num_pages

    try:
        cur_page_items = page_list.page(page)
    except EmptyPage:
        page = total_page
        cur_page_items = page_list.page(page)
    except Exception:
        page = 1
        cur_page_items = page_list.page(page)

    # 页码
    pages = []
    for i in range(page-2, page+3):
        if 0 < i <= total_page:
            pages.append(i)

    res_dict = {
        'list': cur_page_items,
        'cur_page': page,
        'total_page': total_page,
        'pages': pages,
    }
    return res_dict
