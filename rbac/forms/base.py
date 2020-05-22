#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 开发人员   ：Davis Niu
# 开发时间   ：5/8/2020  10:20 PM 
# 文件名称   ：base.PY
from django import forms


class BaseBootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseBootstrapModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
