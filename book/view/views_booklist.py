# coding: utf-8
import traceback

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from el_pagination.decorators import page_template

from book.forms import BookListForm
from book.models import BookList, BookRemark, Book


@page_template('module/_booklist_list.html')
def booklist(request, template='index.html', extra_context=None):
    """
    主页
    :param template: 使用的模板
    :param extra_context: 额外数据
    :param request: 请求
    :return:
    """
    context = {
        'title': '书云',
        'list': BookList.objects.all(),
    }

    # print(get_remote_ip(request))

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context=context)


@page_template('module/_booklistdetail_list.html')
def booklist_detail(request, booklist_id, template='booklist-detail.html', extra_context=None):
    """书单详情"""
    try:
        _booklist = BookList.objects.get(id=booklist_id)
        _books = _booklist.books.all()
        _book_dicts = []
        for _book in _books:
            _book_remark = BookRemark.objects.filter(booklist_id=_booklist.id, book_id=_book.id).first()
            _book_dicts.append((_book, _book_remark))
            # _book_dicts.append({
            #     'book': _book,
            #     'remark': _book_remark,
            # })
        context = {
            'title': '书单 - ' + _booklist.name,
            'list': _book_dicts,
            'booklist': _booklist,
        }
    except BookList.DoesNotExist:
        return render(request, '404page.html')

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context=context)


def add_booklist(request):
    """添加书单"""
    res = {
        "res": "error",
        "msg": "未知错误",
    }

    try:
        if request.method == "POST":
            if request.user.is_authenticated():
                _title = request.POST.get('name')
                _summary = request.POST.get('summary')
                _new_booklist = BookList(name=_title, summary=_summary, user_id=request.user.id)
                try:
                    _new_booklist.save()
                    res["res"] = "success"
                    res["msg"] = ""
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    res["res"] = "error"
                    res["msg"] = "输入不符合要求"
            else:
                res["res"] = "error"
                res["msg"] = "请重新登录"

    except Exception as e:
        print(e)
        traceback.print_exc()
        res["res"] = "error"
        res["msg"] = "未知错误"
    return JsonResponse(res)


def booklist_update(request):
    """书单中书籍评语"""
    res = {
        "res": "error",
        "msg": "未知错误",
    }

    try:
        if request.method == "POST":
            # 使用POST的数据新建Form
            booklist_id = request.POST.get('booklist')
            _booklist = BookList.objects.filter(id=booklist_id).first()
            if _booklist:
                form = BookListForm(request.POST, instance=_booklist)
            else:
                form = BookListForm(request.POST)
            # 验证Form是否合法
            if form.is_valid():
                form.save()
                res["res"] = "success"
                res["msg"] = "添加成功"
            else:
                res["res"] = "error"
                res["msg"] = "字数超限或其他错误"
    except Exception as e:
        print(e)
        traceback.print_exc()
        res["res"] = "error"
        res["msg"] = "未知错误"
    return JsonResponse(res)


@login_required
def booklist_add_book(request):
    """向书单中添加书籍"""
    res = {
        "res": "error",
        "msg": "未知错误",
    }

    try:
        if request.method == "POST":
            # print(request.POST)
            # 使用POST的数据新建Form
            _book_id = request.POST.get('book')
            _booklist_id = request.POST.get('booklist')
            _remark = request.POST.get('remark')
            _book = Book.objects.filter(id=_book_id).first()
            _booklist = BookList.objects.filter(id=_booklist_id).first()
            if _booklist and _book:
                if _book in _booklist.books.all():
                    res["res"] = "error"
                    res["msg"] = "书籍已存在"
                else:
                    _booklist.books.add(_book)
                    _booklist.save()

                    try:
                        # 添加评语
                        _book_remark = BookRemark.objects.filter(booklist_id=_booklist.id, book_id=_book.id).first()
                        if _book_remark:
                            _book_remark.content = _remark
                        else:
                            _book_remark = BookRemark(booklist_id=_booklist.id, book_id=_book.id, content=_remark)
                        _book_remark.save()
                    except Exception as e:
                        print(e)
                        traceback.print_exc()

                    res["res"] = "success"
                    res["msg"] = ""
            elif not _book:
                res["res"] = "error"
                res["msg"] = "书籍不存在"
            elif not _booklist:
                res["res"] = "error"
                res["msg"] = "书单不存在"
    except Exception as e:
        print(e)
        traceback.print_exc()
        res["res"] = "error"
        res["msg"] = "未知错误"
    return JsonResponse(res)


@login_required
def booklist_delete_book(request):
    """向书单中删除书籍"""
    res = {
        "res": "error",
        "msg": "未知错误",
    }

    try:
        if request.method == "POST":
            # 使用POST的数据新建Form
            _book_id = request.POST.get('book')
            _booklist_id = request.POST.get('booklist')
            _book = Book.objects.filter(id=_book_id).first()
            _booklist = BookList.objects.filter(id=_booklist_id).first()
            if _booklist and _book:
                if _book in _booklist.books.all():
                    _booklist.books.remove(_book)
                    res["res"] = "success"
                    res["msg"] = "书籍已存在"
                else:
                    res["res"] = "error"
                    res["msg"] = "书单中不存在该书籍"
            elif not _book:
                res["res"] = "error"
                res["msg"] = "书籍不存在"
            elif not _booklist:
                res["res"] = "error"
                res["msg"] = "书单不存在"
    except Exception as e:
        print(e)
        traceback.print_exc()
        res["res"] = "error"
        res["msg"] = "未知错误"
    return JsonResponse(res)


@login_required
def booklist_delete(request):
    """书单中书籍评语"""
    res = {
        "res": "error",
        "msg": "未知错误",
    }

    try:
        if request.method == "POST":
            # 使用POST的数据新建Form
            booklist_id = request.POST.get('booklist')
            _booklist = BookList.objects.get(id=booklist_id)
            if _booklist:
                _booklist.delete()
                res["res"] = "success"
                res["msg"] = "删除成功"
            else:
                res["res"] = "error"
                res["msg"] = "书单不存在"
    except Exception as e:
        print(e)
        traceback.print_exc()
        res["res"] = "error"
        res["msg"] = "未知错误"
    return JsonResponse(res)

