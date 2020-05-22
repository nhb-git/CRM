#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：5/6/2020  08:22 AM 
# 文件名称   ：user.PY
from django.shortcuts import render, redirect, reverse, HttpResponse
from rbac import models
from rbac.forms import user


def user_list(request):
    users_queryset = models.UserInfo.objects.all()
    return render(request, 'rbac/user_list.html', {'users': users_queryset})


def user_add(request):
    if request.method == 'GET':
        form = user.AddUser()
        return render(request, 'rbac/user_change.html', {'form': form})
    form = user.AddUser(data=request.POST)
    if form.is_valid():
        user_obj = {
            'name': request.POST.get('name'),
            'password': request.POST.get('pwd'),
            'email': request.POST.get('email')
        }
        models.UserInfo.objects.create(**user_obj)
        return redirect(reverse('rbac:user_list'))
    else:
        print(form.errors.get('__all__'))
        return render(request, 'rbac/user_change.html', {'form': form, 'pass_diff_error': form.errors.get('__all__')})


def user_edit(request, user_id):
    user_obj = models.UserInfo.objects.filter(pk=user_id).first()
    if not user_obj:
        return HttpResponse('用户不存在')
    if request.method == 'GET':
        form = user.UpdateUserModelForm(instance=user_obj)
        return render(request, 'rbac/user_change.html', {'form': form})
    form = user.UpdateUserModelForm(instance=user_obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/user_change.html', {'form': form})


def user_del(request, user_id):
    origin_url = reverse('rbac:user_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})
    models.UserInfo.objects.filter(pk=user_id).delete()
    return redirect(reverse('rbac:user_list'))


def reset_pwd(request, user_id):
    user_obj = models.UserInfo.objects.filter(pk=user_id).first()
    if not user_obj:
        return HttpResponse('用户不存在')
    if request.method == 'GET':
        form = user.UpdatePasswordModelForm()
        return render(request, 'rbac/user_change.html', {'form': form})
    form = user.UpdatePasswordModelForm(instance=user_obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/user_change.html', {'form': form})
