#! /usr/bin/env python
# coding:utf-8
"""
Created on: 2017-03-09 18:01 
@author: guolt
"""

from django.conf.urls import url,include

from .views import UserInfoView,UploadImageView,UpdatePwdView,SendEmailCodeView,UpdateEmailView

urlpatterns = [
    #用户中心
    url(r'^info/$', UserInfoView.as_view(),name="user_info"),
    #用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(),name="image_upload"),
    #用户密码更新
    url(r'^update/pwd/$', UpdatePwdView.as_view(),name="update_pwd"),
    #发送邮箱的验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(),name="sendemail_code"),
    #更新邮箱的验证码
    url(r'^update_email/$', UpdateEmailView.as_view(),name="update_email"),
]


