# coding: utf-8
# File: user_views.py
# Intro: 用户相关views
# Author: szhkai@qq.com
import traceback

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from el_pagination.decorators import page_template

from book.forms import UserForm
from book.models import BookList


def user_register(request):
    """用户注册"""
    res = {
        "res": "error",
        "msg": "未知错误",
    }

    if request.method == "POST":
        # 使用POST的数据新建用户Form
        form = UserForm(request.POST)
        # 验证是否输入合法
        if form.is_valid():
            user = form.save(commit=False)

            # cleaned data
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

            res["res"] = "success"
            res["msg"] = "注册成功"
        else:
            res["res"] = "error"
            res["msg"] = "用户已存在/信息输入不符合格式"

    return JsonResponse(res)


def user_login(request):
    """用户登录"""
    res = {
        "res": "error",
        "msg": "未知错误",
    }

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                res["res"] = "success"
                res["msg"] = ""
        else:
            res["res"] = "error"
            res["msg"] = "用户名/密码错误"

    return JsonResponse(res)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


@page_template('module/_booklist_list.html')
def user_page(request, user_id=None, template='user-page.html', extra_context=None):
    """
    主页
    :param user_id:
    :param template: 使用的模板
    :param extra_context: 额外数据
    :param request: 请求
    :return:
    """
    try:
        if not user_id:
            if request.user.is_authenticated():
                user_id = request.user.id
            else:
                return render(request, '404page.html')
        _user = User.objects.filter(id=user_id).first()
        if not _user:
            return render(request, '404page.html')

        context = {
            'title': '个人主页',
            'list': BookList.objects.filter(user_id=user_id),
            'user': _user
        }

        if extra_context is not None:
            context.update(extra_context)

        return render(request, template, context=context)
    except Exception as e:
        print(e)
        traceback.print_exc()
        return render(request, '404page.html')


@login_required
def user_profile(request):
    """用户信息"""
    try:
        return render(request, 'user-profile.html')
    except Exception as e:
        print(e)
        return render(request, '404page.html')


@login_required
def user_profile_update(request):
    """更新用户信息"""
    res = {
        "res": "error",
        "msg": "未知错误",
    }

    try:
        if request.method == "POST":
            _nickname = request.POST.get('nickname')
            _password = request.POST.get('password')
            _new_password = request.POST.get('newPassword')
            _new_password_repeat = request.POST.get('newPasswordRepeat')

            _user = User.objects.filter(id=request.user.id).first()
            if _user:
                _user.nickname = _nickname
                _user.save()
                res["res"] = "success"
                res["msg"] = "修改昵称成功!"

            if len(_new_password) != 0:
                user = authenticate(username=request.user.username, password=_password)
                if user:
                    if _new_password != _new_password_repeat:
                        res["res"] = "error"
                        res["msg"] = "两次输入的密码不一致!"
                    else:
                        user.set_password(_new_password)
                        user.save()
                        login(request, user)
                        res["res"] = "success"
                        res["msg"] = "修改密码成功!"
                else:
                    res["res"] = "error"
                    res["msg"] = "用户认证失败, 密码输入错误?"
    except Exception as e:
        print(e)
        traceback.print_exc()
    return JsonResponse(res)
