# -*- coding: utf-8 -*-
__author__ = 'shine_forever'
__date__ = '2017/2/9 22:14'
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)


