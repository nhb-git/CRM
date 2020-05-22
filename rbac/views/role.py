#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：5/5/2020  11:32 AM 
# 文件名称   ：role.PY
from django.shortcuts import render, HttpResponse, redirect, reverse
from rbac import models
from rbac.forms import role


def role_list(request):
    """
    角色列表
    :param request:
    :return:
    """
    role_queryset = models.Role.objects.all()
    return render(request, 'rbac/role_list.html', {'roles': role_queryset})


def role_add(request):
    if request.method == 'GET':
        form = role.AddRole()
        return render(request, 'rbac/role_change.html', {'form': form})
    form = role.AddRole(data=request.POST)
    if form.is_valid():
        role_obj = {'title': request.POST.get('title')}
        models.Role.objects.create(**role_obj)
        return redirect(reverse('rbac:role_list'))
    else:
        return render(request, 'rbac/role_change.html', {'form': form})


def role_edit(request, role_id):
    """
    角色编辑
    :param request:
    :param role_id: 角色的id
    :return:
    """
    role_obj = models.Role.objects.filter(id=role_id).first()
    if role_obj:
        if request.method == 'GET':
            form = role.AddRole(initial={'title': role_obj.title})
        if request.method == 'POST':
            form = role.AddRole(request.POST)
            if form.is_valid():
                models.Role.objects.filter(id=role_id).update(title=request.POST.get('title'))
                return redirect(reverse('rbac:role_list'))
        return render(request, 'rbac/role_change.html', {'form': form})
    else:
        return HttpResponse('角色不存在')


def role_del(request, role_id):
    """
    删除角色
    :param request:
    :param role_id: 角色id
    :return:
    """
    origin_url = reverse('rbac:role_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})
    models.Role.objects.filter(id=role_id).delete()
    return redirect(origin_url)
