#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：5/6/2020  09:22 PM 
# 文件名称   ：user.PY
from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from rbac import models


class AddUser(forms.Form):
    name = forms.CharField(
        label='用户名', min_length=3, max_length=16, error_messages={
            'required': '用户名不能为空',
            'min_length': '用户名至少3位',
            'max_length': '用户名最多16位',
        },
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '用户名',
            }
        )
    )
    email = forms.EmailField(
        label='邮箱', max_length=64, error_messages={
            'max_length': '邮箱最多64位字符长度',
            'required': '邮箱必填',
        },
        widget=widgets.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': '邮箱'
            }
        )
    )
    pwd = forms.CharField(
        label='密码', min_length=6, max_length=64, error_messages={
            'required': '密码不能为空',
            'min_length': '密码至少6位',
            'max_length': '密码最多64位',
        },
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '密码',
            }
        )
    )
    re_pwd = forms.CharField(
        label='重复密码', min_length=6, max_length=64, error_messages={
            'required': '密码不能为空',
            'min_length': '密码至少6位',
            'max_length': '密码最多64位',
        },
        widget=widgets.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '重复密码',
            }
        )
    )

    def clean_name(self):
        val = self.cleaned_data.get('name')
        ret = models.UserInfo.objects.filter(name=val)
        if not ret:
            return val
        else:
            raise ValidationError('用户已存在')

    def clean_email(self):
        val = self.cleaned_data.get('email')
        ret = models.UserInfo.objects.filter(email=val)
        if not ret:
            return val
        else:
            raise ValidationError('邮箱已被使用')

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')
        if pwd and re_pwd:
            if pwd == re_pwd:
                return self.cleaned_data
            else:
                raise ValidationError('两次密码不一致')
        else:
            return self.cleaned_data


class UpdateUserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'email']

        error_messages = {
            'name': {
                'required': '用户名不能为空',
            },
            'email': {
                'required': '邮箱不能为空',
            }

        }

    def __init__(self, *args, **kwargs):
        super(UpdateUserModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UpdatePasswordModelForm(forms.ModelForm):
    confirmed_password = forms.CharField(label='重复密码')

    class Meta:
        model = models.UserInfo
        fields = ['password', 'confirmed_password']

    def __init__(self, *args, **kwargs):
        super(UpdatePasswordModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_confirmed_password(self):
        password = self.cleaned_data.get('password')
        confirmed_password = self.cleaned_data.get('confirmed_password')
        if password and confirmed_password:
            if password == confirmed_password:
                return confirmed_password
            else:
                raise ValidationError('两次密码不一致')
        else:
            return confirmed_password
