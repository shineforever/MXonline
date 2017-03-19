#! /usr/bin/env python
# coding:utf-8
"""
Created on: 2017-03-09 18:01 
@author: guolt
"""

from django.conf.urls import url,include

from .views import UserInfoView,UploadImageView,UpdatePwdView,SendEmailCodeView,UpdateEmailView,MyCourse,MyFavOrg,MyFavTeacher,MyMessage

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
    #我的课程
    url(r'^mycourse/$', MyCourse.as_view(),name="mycourse"),
    #我收藏的课程机构
    url(r'^myfav/org/$', MyFavOrg.as_view(),name="myfav_org"),
    #我收藏的老师
    url(r'^myfav/teacher/$', MyFavTeacher.as_view(),name="myfav_teacher"),
    #我的消息
    url(r'^mymessage/$', MyMessage.as_view(),name="my_message"),
]


