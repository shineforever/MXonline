#! /usr/bin/env python
# coding:utf-8
"""
Created on: 2017-02-21 16:13 
@author: guolt
"""
from django.conf.urls import url,include

from .views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView


urlpatterns = [
    #课程机构列表
    url(r'^list/$', OrgView.as_view(),name="org-list"),
    url(r'^add_ask/$', AddUserAskView.as_view(),name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(),name="org_home"),
    url(r'^course/(?P<course_id>\d+)/$', OrgCourseView.as_view(),name="org_course")
]

