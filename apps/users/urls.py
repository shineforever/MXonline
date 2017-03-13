#! /usr/bin/env python
# coding:utf-8
"""
Created on: 2017-03-09 18:01 
@author: guolt
"""

from django.conf.urls import url,include

from .views import UserInfoView,UploadImageView,UpdatePwdView


urlpatterns = [
    #用户中心
    url(r'^info/$', UserInfoView.as_view(),name="user_info"),
    #用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(),name="image_upload"),
    #用户密码更新
    url(r'^update/pwd/$', UpdatePwdView.as_view(),name="update_pwd"),

]


