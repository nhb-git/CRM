#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：5/7/2020  03:36 PM 
# 文件名称   ：menu.PY
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from rbac import models
from rbac.forms.base import BaseBootstrapModelForm


class FirstMenuModelForm(BaseBootstrapModelForm):
    class Meta:
        model = models.Permission
        fields = ['title', 'icon', 'alias']

        labels = {
            'title': '一级菜单名称',
            'icon': '图标',
            'alias': '菜单别名',
        }
        error_messages = {
            'title': {
                'required': '菜单名称不能为空'
            },
            'icon': {
                'required': '图标不能为空'
            },
            'alias': {
                'required': '别名不能为空'
            }
        }

    # 已使用基类替代
    # def __init__(self, *args, **kwargs):
    #     super(FirstMenuModelForm, self).__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'

    def clean_title(self):
        val = self.cleaned_data.get('title')
        ret = models.Permission.objects.filter(title=val)
        if not ret:
            return val
        else:
            raise ValidationError('菜单名称已经存在')

    def clean_alias(self):
        val = self.cleaned_data.get('alias')
        ret = models.Permission.objects.filter(alias=val)
        if not ret:
            return val
        else:
            raise ValidationError('别名不唯一，请重新填写')


class SecondModelForm(forms.ModelForm):
    class Meta:
        model = models.Permission
        exclude = ['icon']
        labels = {
            'title': '菜单或非菜单名称',
            'url': '路径',
            'is_menu': '是否作为菜单',
            'alias': '菜单或非菜单权限别名',
            'parent_menu': '父菜单',
        }

        error_messages = {
            'title': {
                'required': '名称不能为空'
            },
            'url': {
                'required': '路径不能为空'
            },
            'alias': {
                'required': '别名不能为空'
            },
            'parent_menu': {
                'required': '父菜单必填'
            }
        }
        widgets = {
            'title': widgets.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'url': widgets.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'alias': widgets.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'parent_menu': widgets.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
