#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：4/29/2020  09:18 AM 
# 文件名称   ：init_permission.PY
from django.conf import settings


def init_permission(request, user_obj):
    """
    用户权限初始化
    :param request: 用户请求对象
    :param user_obj: 当前用户
    :return:
    """
    permission_queryset = user_obj.roles.filter(permissions__isnull=False).values('permissions__url',
                                                                                  'permissions__title',
                                                                                  'permissions__alias',
                                                                                  'permissions__is_menu',
                                                                                  'permissions__icon',
                                                                                  'permissions__parent_menu',
                                                                                  'permissions__parent_menu__title',
                                                                                  'permissions__parent_menu__url',
                                                                                  'permissions__id',).distinct()
    menu_list = []
    permission_dict = {}
    for item in permission_queryset:
        permission_dict[item['permissions__alias']] = {
                'id': item.get('permissions__id'),
                'url': item.get('permissions__url'),
                'title': item.get('permissions__title'),
                'parent_menu_id': item.get('permissions__parent_menu'),
                'parent_menu_title': item.get('permissions__parent_menu__title'),
                'parent_menu_url': item.get('permissions__parent_menu__url')
            }
        if item.get('permissions__is_menu'):
            menu_list.append(
                {
                    'id': item.get('permissions__id'),
                    'title': item.get('permissions__title'),
                    'url': item.get('permissions__url'),
                    'icon': item.get('permissions__icon'),
                    'parent_menu': item.get('permissions__parent_menu'),
                }
            )
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_list
