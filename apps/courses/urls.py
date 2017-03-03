# -*- coding: utf-8 -*-
__author__ = 'shine_forever'
__date__ = '2017/2/26 11:18'

from django.conf.urls import url,include
from .views import CourseListView,CourseDetailView,CourseInfoView,CommentView,AddCommentsView,VideoPlayView

urlpatterns = [
    #课程列表
    url(r'^list/$', CourseListView.as_view(),name="course_list"),
    #课程的详情
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(),name="course_detail"),
    #课程章节信息
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(),name="course_info"),
    #课程评论页面
    url(r'^comment/(?P<course_id>\d+)/$', CommentView.as_view(), name="course_comment"),
    #添加课程评论
    url(r'^add_comment/$', AddCommentsView.as_view(), name="add_comment"),
    #视频播放
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name="video_play")
]

