#! /usr/bin/env python
# coding:utf-8
"""
Created on: 2017-03-09 18:01 
@author: guolt
"""

from django.conf.urls import url,include

from .views import UserInfoView


urlpatterns = [
    #用户中心
    url(r'^info/$', UserInfoView.as_view(),name="user_info"),

]


