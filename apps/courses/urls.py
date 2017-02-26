# -*- coding: utf-8 -*-
__author__ = 'shine_forever'
__date__ = '2017/2/26 11:18'

from django.conf.urls import url,include
from .views import CourseListView

urlpatterns = [
    #课程列表
    url(r'^list/$', CourseListView.as_view(),name="course_list"),

]

