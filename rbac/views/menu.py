#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：5/7/2020  10:12 AM 
# 文件名称   ：menu.PY
import re
from django.shortcuts import render, HttpResponse, redirect, reverse
from rbac import models
from rbac.forms import menu
from django.conf import settings
from django.utils.module_loading import import_string
from collections import OrderedDict
from django.urls import RegexURLPattern, RegexURLResolver


def menu_list(request):
    """
    菜单和权限列表
    :param request:
    :return:
    """
    menu_id = request.GET.get('mid')
    second_menu_id = request.GET.get('sid')
    if models.Permission.objects.filter(id=menu_id).exists():
        second_menu = models.Permission.objects.filter(parent_menu_id=menu_id, parent_menu__isnull=False)
    else:
        second_menu = []
        menu_id = None
    first_menu = models.Permission.objects.filter(is_menu=True, parent_menu_id=None)
    return render(request, 'rbac/menu_list.html', {
            'first_menu': first_menu, 'mid': menu_id, 'second_menu': second_menu, 'sid': second_menu_id
        }
    )


def menu_add(request, level):
    """
    添加菜单和非菜单
    :param request:
    :param level: first, second
    :return:
    """
    level_list = ['first', 'second']
    if level in level_list:
        if request.method == 'GET':
            # 渲染一级菜单
            if level == level_list[0]:
                form = menu.FirstMenuModelForm()
            # 渲染二级菜单和非菜单
            if level == level_list[1]:
                for params in request.GET.get('_filter').split('&'):
                    param = params.split('=')
                    if 'mid' in param:
                        parent_menu_id = param[1]
                form = menu.SecondModelForm(initial={'parent_menu': parent_menu_id})
            return render(request, 'rbac/change.html', {'form': form})

        url_args = request.GET.get('_filter')
        url = (reverse('rbac:menu_list') + '?' + url_args) if url_args else reverse('rbac:menu_list')
        if level == level_list[0]:
            form = menu.FirstMenuModelForm(data=request.POST)
            if form.is_valid():
                menu_obj = {
                    'title': request.POST.get('title'), 'is_menu': True,
                    'icon': request.POST.get('icon'), 'alias': request.POST.get('alias')
                }
                models.Permission.objects.create(**menu_obj)
                return redirect(url)
        if level == level_list[1]:
            form = menu.SecondModelForm(data=request.POST)
            if form.is_valid():
                form.save()
                return redirect(url)
        return render(request, 'rbac/change.html', {'form': form})


def menu_edit(request, level, menu_id):
    """
    编辑菜单
    :param request:
    :param level:
    :param menu_id:
    :return:
    """
    level_list = ['first', 'second']
    if level in level_list:
        menu_obj = models.Permission.objects.filter(id=menu_id).first()
        if request.method == 'GET':
            if not menu_obj:
                return HttpResponse('菜单不存在')
            if level == level_list[0]:
                form = menu.FirstMenuModelForm(instance=menu_obj)
            if level == level_list[1]:
                form = menu.SecondModelForm(instance=menu_obj)
            return render(request, 'rbac/change.html', {'form': form})
        if level == level_list[0]:
            form = menu.FirstMenuModelForm(instance=menu_obj, data=request.POST)
        if level == level_list[1]:
            form = menu.SecondModelForm(instance=menu_obj, data=request.POST)
        if form.is_valid():
            form.save()
            url_args = request.GET.get('_filter')
            url = (reverse('rbac:menu_list')+'?'+url_args) if url_args else reverse('rbac:menu_list')
            return redirect(url)
        return render(request, 'rbac/change.html', {'form': form})


def menu_del(request, level, menu_id):
    """
    删除菜单
    :param request:
    :param level:
    :param menu_id:
    :return:
    """
    level_list = ['first', 'second']
    origin_url = reverse('rbac:menu_list')
    url_args = request.GET.get('_filter')
    url = (origin_url+'?'+url_args) if url_args else origin_url
    if level in level_list:
        if request.method == 'GET':
            return render(request, 'rbac/delete.html', {'cancel': url})
        models.Permission.objects.filter(id=menu_id).delete()
        return redirect(origin_url)


def check_url_exclude(url):
    exclude_url = [
        '/admin/.*',
        '/login/.*',
    ]
    for regex in exclude_url:
        if re.match(regex, url):
            return True


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
    递归的获取所有url
    :param pre_namespace: namespace前缀，以后用户用于拼接name
    :param pre_url: url前缀，以后用于拼接url
    :param urlpatterns: 路由关系列表
    :param url_ordered_dict: 用户保存所有路由
    :return:
    """
    for item in urlpatterns:
        if isinstance(item, RegexURLPattern):
            if not item.name:
                continue
            if pre_namespace:
                name = '{0}:{1}'.format(pre_namespace, item.name)
            else:
                name = item.name

            url = pre_url + item._regex     # /^rbac/^test/$
            url = url.replace('^', '').replace('$', '')
            if check_url_exclude(url):
                continue
            url_ordered_dict[name] = {'name': name, 'url': url}
        elif isinstance(item, RegexURLResolver):
            if pre_namespace:
                if item.namespace:
                    namespace = '%s:%s' % (pre_namespace, item.namespace)
                else:
                    # namespace = item.namespace
                    namespace = None
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            recursion_urls(namespace, pre_url + item.regex.pattern, item.url_patterns, url_ordered_dict)


def get_all_url():
    """
    获取所有的url
    :return:
    """
    url_order_dict = OrderedDict()
    md = import_string(settings.ROOT_URLCONF)
    recursion_urls(None, '/', md.urlpatterns, url_order_dict)
    return url_order_dict


def multi_permission(request):
    all_url_dict = get_all_url()
    # 获取自动发现的所有name
    router_name_set = set(all_url_dict.keys())

    # 获取数据库中的所有name
    permissions = models.Permission.objects.all().values(
        'id', 'title', 'url', 'is_menu', 'icon', 'alias', 'parent_menu_id'
    )
    return HttpResponse('ok')
