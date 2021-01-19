import json
import traceback
from urllib.error import HTTPError

from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from el_pagination.decorators import page_template

from book.forms import BookRemarkForm
from book.models import Book, BookList, BookRemark
from book.mytools import get_remote_ip
from book.view.func.modal_utails import trance_authors_to_list, trance_tags_to_list
# Create your views here.
from spider.douban.api.douban_api import get_douban_book_by_url


@page_template('module/_book_list.html')
def find(request, template='find.html', extra_context=None):
    context = {
        'title': '发现',
        'list': Book.objects.all(),
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context=context)


def book_remark(request):
    """书单中书籍评语"""
    res = {
        "res": "error",
        "msg": "未知错误",
    }

    try:
        if request.method == "POST":
            # 使用POST的数据新建Form
            booklist_id = request.POST.get('booklist')
            book_id = request.POST.get('book')
            _bookremark = BookRemark.objects.filter(booklist_id=booklist_id, book_id=book_id).first()
            if _bookremark:
                form = BookRemarkForm(request.POST, instance=_bookremark)
            else:
                form = BookRemarkForm(request.POST)
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
        res["msg"] = "保存时出错"
    return JsonResponse(res)


def get_douban_book_from_url(request):
    """从POST中获取豆瓣图书url, 返回该书籍的一些信息, 如果不存在则爬取"""
    res = {
        "res": "error",
        "msg": "未知错误",
    }
    try:
        _book_url = request.POST.get("url")
        _book = get_douban_book_by_url(_book_url, use_proxy=False)
        if _book is not None and isinstance(_book, Book):
            # 获取成功

            # 获取author
            # 获取tag

            _return_data = {
                'id': _book.id,
                'name': _book.name,
                'score': _book.score.score,
                'author': trance_authors_to_list(_book.author.all()),
                'pic': _book.pic,
                'tag': trance_tags_to_list(_book.tags.all()),
                'summary': _book.summary,
            }
            res["res"] = "success"
            res["msg"] = ""
            res["data"] = _return_data
        else:
            res["res"] = "error"
            res["msg"] = "从豆瓣获取图书信息失败"
    except HTTPError:
        res["res"] = "error"
        res["msg"] = "从豆瓣获取图书信息失败"
    except Exception as e:
        print(e)
        traceback.print_exc()
        res["res"] = "error"
        res["msg"] = "未知错误"
    return JsonResponse(res)


def user_booklist_get(request):
    """获取当前用户书单列表"""
    res = {
        "res": "error",
        "msg": "未知错误",
    }

    try:
        # _user = User.objects.filter(username="szhkai").first()
        if request.method == "POST":
            if request.user.is_authenticated:
                _booklists = BookList.objects.filter(user_id=request.user.id)
                res["res"] = "success"
                res["msg"] = ""
                res["data"] = json.loads(serializers.serialize("json", _booklists, fields=("id", "name")))
            else:
                res["res"] = "error"
                res["msg"] = "未登录"
    except Exception as e:
        print(e)
        traceback.print_exc()
        res["res"] = "error"
        res["msg"] = "未知错误"
    return JsonResponse(res)


def book_add_to_booklists(request):
    """将书籍添加到多个书单"""
    res = {
        "res": "error",
        "msg": "未知错误",
    }

    try:
        # _user = User.objects.filter(username="szhkai").first()
        if request.method == "POST":
            # print(request.POST)
            if request.user.is_authenticated:
                _book_id = request.POST.get("book")
                _booklist_ids = request.POST.getlist("booklists[]")
                _remark = request.POST.get("remark")
                if _remark:
                    _remark = str(_remark).strip()
                _book = Book.objects.filter(id=_book_id).first()

                if not _book:
                    res["res"] = "error"
                    res["msg"] = "书籍不存在"
                else:
                    # 循环书单
                    res["res"] = "success"
                    res["msg"] = ""

                    for _booklist_id in _booklist_ids:
                        _t_booklist = BookList.objects.filter(id=_booklist_id).first()
                        if _t_booklist:
                            if _t_booklist.user.id == request.user.id and _book not in _t_booklist.books.all():
                                _t_booklist.books.add(_book)
                                # 添加评语
                                if len(_remark) > 0:
                                    try:
                                        _book_remark = BookRemark.objects.filter(booklist_id=_t_booklist.id,
                                                                                 book_id=_book.id).first()
                                        if _book_remark:
                                            _book_remark.content = _remark
                                        else:
                                            _book_remark = BookRemark(booklist_id=_t_booklist.id, book_id=_book.id,
                                                                      content=_remark)
                                        # 保存
                                        _book_remark.save()
                                    except Exception as e:
                                        print(e)
                                        traceback.print_exc()

                            else:
                                res["res"] = "error"
                                res["msg"] = "部分书籍添加失败"
            else:
                res["res"] = "error"
                res["msg"] = "未登录"
    except Exception as e:
        print(e)
        traceback.print_exc()
        res["res"] = "error"
        res["msg"] = "未知错误"
    return JsonResponse(res)


@page_template('entry_list_page.html')
def test(request, template='index_entry.html', extra_context=None):
    """流式加载分页"""
    context = {
        'entry_list': BookList.objects.all()
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


def your_ip(request):
    return HttpResponse(get_remote_ip(request))
