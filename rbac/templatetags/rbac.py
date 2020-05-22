#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：4/29/2020  06:00 PM 
# 文件名称   ：rbac.PY
from django.template import Library
from django.conf import settings
from django.http import QueryDict
from django.shortcuts import reverse


register = Library()


@register.inclusion_tag('rbac/static_menu.html')
def static_menu(request):
    """
    一级菜单
    :param request:
    :return:
    """
    menu_list = request.session.get(settings.MENU_SESSION_KEY)
    current_url = request.path_info
    return {'menu_list': menu_list, 'current_url': current_url}


@register.inclusion_tag('rbac/sub_menu.html')
def sub_menu(request):
    """
    二级菜单
    :param request:
    :return:
    """
    menu_info = request.session.get(settings.MENU_SESSION_KEY)
    menu_list = []
    current_url = request.path_info

    # 获取所有的父菜单
    parent_menu_list = []
    for menu_item in menu_info:
        menu_node = {
            'id': menu_item.get('id'), 'url': menu_item.get('url'), 'title': menu_item.get('title'),
            'icon': menu_item.get('icon'), 'child': []
        }
        if not menu_item.get('parent_menu'):
            if menu_item.get('id') == request.current_access_url_parent_id:
                menu_node['class'] = ''
            else:
                menu_node['class'] = 'hide'
            parent_menu_list.append(menu_node)

    # 获取所有父菜单对应的子菜单
    for parent_menu_item in parent_menu_list:
        for menu_item in menu_info:
            menu_node = {
                'id': menu_item.get('id'), 'url': menu_item.get('url'), 'title': menu_item.get('title'),
                'icon': menu_item.get('icon'), 'child': []
            }
            if menu_item.get('parent_menu') and (menu_item.get('parent_menu') == parent_menu_item.get('id')):
                parent_menu_item.get('child').append(menu_node)
        menu_list.append(parent_menu_item)
    return {'menu_list': menu_list, 'current_url': current_url}


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    """
    导航路径
    :param request:
    :return: dict
    """
    return {'url_record': request.url_record}


@register.filter
def has_permission(request, alias):
    """
    判断是否有权限
    :param request:
    :param alias:
    :return:
    """
    if alias in request.session[settings.PERMISSION_SESSION_KEY]:
        return True


@register.simple_tag
def memory_url(request, name, *args, **kwargs):
    """
    生成带原参数的url
    :param request:
    :param name:
    :param args:
    :return:
    """
    basic_url = reverse(name, args=args)

    # 当url无参数时
    if not request.GET:
        return basic_url
    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()
    return '%s?%s' % (basic_url, query_dict.urlencode())
