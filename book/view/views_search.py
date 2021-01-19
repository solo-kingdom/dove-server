# coding: utf-8
import traceback

from django.shortcuts import render, redirect
from el_pagination.decorators import page_template

from book.view.func.search import solve_search_booklist, solve_search_book

search_booklist_recommend = {'name': 'booklist', 'tip': '书单'}
search_book_recommend = {'name': 'book', 'tip': '书籍'}
search_book_tag_recommend = {'name': 'book-tag', 'tip': '书籍'}
search_booklist_tag_recommend = {'name': 'booklist-tag', 'tip': '书籍'}


@page_template('module/_booklist_list.html')
def search_booklist(request, template='search.html', extra_context=None):
    search_keyword = request.session['search_keyword']
    context = {
        'title': '搜索书单',
        'list': solve_search_booklist(search_keyword),
        'search_keyword': search_keyword,
        'search_type_cur': search_booklist_recommend,
        'search_type_recommend': [search_book_recommend, ],
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context=context)


@page_template('module/_book_list.html')
def search_book(request, template='search.html', extra_context=None):
    search_keyword = request.session['search_keyword']
    context = {
        'title': '搜索书籍',
        'list': solve_search_book(search_keyword),
        'search_keyword': search_keyword,
        'search_type_cur': search_book_recommend,
        'search_type_recommend': [search_booklist_recommend, ],
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context=context)


def search(request):
    try:
        search_keyword = request.POST.get('search_keyword')
        search_type = request.POST.get('search_type')

        if search_keyword:
            request.session['search_keyword'] = search_keyword
            request.session['search_type'] = search_type
        else:
            search_type = request.session['search_type']

        if search_type == 'book':
            # 搜索图书
            return redirect(search_book)
        else:
            # 默认搜索列表
            return redirect(search_booklist)

            # return render(request, template, context=context)
    except Exception as e:
        print(e)
        traceback.print_exc()
    return render(request, '404page.html')
