#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：4/29/2020  09:34 AM 
# 文件名称   ：rbac.PY
import re
from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """
    def process_request(self, request):
        """
        用户请求进入时触发执行
        :param request:
        :return:
        """
        """
        1. 获取用户请求的url
        2. 获取当前用户的权限列表
        3. url校验
        """
        current_url = request.path_info
        url_record = [
            {'title': '首页', 'url': ''},
        ]
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        # 白名单权限验证
        for url in settings.VALID_URL_LIST:
            reg = '^{0}$'.format(url)
            if re.match(reg, current_url):
                return None

        for permission_item in permission_dict.values():
            reg = '^{0}$'.format(permission_item.get('url'))
            if re.match(reg, current_url):
                if permission_item.get('parent_menu_id'):
                    url_record.extend([
                        {'title': permission_item.get('parent_menu_title'), 'url': permission_item.get('parent_menu_url')},
                        {'title': permission_item.get('title'), 'url': permission_item.get('url')},
                    ])
                else:
                    url_record.extend([
                        {'title': permission_item.get('title'), 'url': permission_item.get('url')},
                    ])
                request.url_record = url_record
                request.current_access_url_parent_id = permission_item.get('parent_menu_id') or permission_item.get('id')
                return None
        else:
            return HttpResponse('无权访问')
