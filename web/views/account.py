#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：4/28/2020  09:38 PM 
# 文件名称   ：account.PY
# 开发工具   ：PyCharm


from django.shortcuts import HttpResponse, render, redirect
from django.http import JsonResponse
from rbac import models
from rbac.service.init_permission import init_permission


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    # 账户密码校验
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    user_obj = models.UserInfo.objects.filter(name=user, password=pwd).first()
    if not user_obj:
        return render(request, 'login.html', {'msg': '用户名或密码错误'})
    # 根据用户信息获取用户拥有的所有权限, 并放入session
    init_permission(request, user_obj)

    return redirect('/customer/list/')
