#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：5/5/2020  11:29 AM 
# 文件名称   ：urls.PY
from django.conf.urls import url
from rbac.views import role, user, menu


urlpatterns = [
    # 角色管理
    url(r'^role/list/$', role.role_list, name='role_list'),
    url(r'^role/add/$', role.role_add, name='role_add'),
    url(r'^role/edit/(?P<role_id>\d+)/$', role.role_edit, name='role_edit'),
    url(r'^role/del/(?P<role_id>\d+)/$', role.role_del, name='role_del'),

    # 用户管理
    url(r'user/list/$', user.user_list, name='user_list'),
    url(r'user/add/$', user.user_add, name='user_add'),
    url(r'user/edit/(?P<user_id>\d+)/$', user.user_edit, name='user_edit'),
    url(r'user/del/(?P<user_id>\d+)/$', user.user_del, name='user_del'),
    url(r'user/reset/pwd/(?P<user_id>\d+)/$', user.reset_pwd, name='reset_pwd'),

    # 菜单管理
    url(r'menu/list/$', menu.menu_list, name='menu_list'),
    url(r'menu/add/(?P<level>first|second)/$', menu.menu_add, name='menu_add'),
    url(r'menu/edit/(?P<level>first|second)/(?P<menu_id>\d+)/$', menu.menu_edit, name='menu_edit'),
    url(r'menu/del/(?P<level>first|second)/(?P<menu_id>\d+)/$', menu.menu_del, name='menu_del'),
    url(r'menu/mul/$', menu.multi_permission, name='multi_permission'),
]
