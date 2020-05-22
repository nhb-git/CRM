#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：5/5/2020  04:37 PM 
# 文件名称   ：role.PY
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from rbac import models


class AddRole(forms.Form):
    title = forms.CharField(
        label='角色名称',
        error_messages={'required': '角色名不能为空'},
        widget=widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    def clean_title(self):
        val = self.cleaned_data.get('title')
        ret = models.Role.objects.filter(title=val)
        if not ret:
            return val
        else:
            raise ValidationError('角色已经存在, 请更换角色名称')
