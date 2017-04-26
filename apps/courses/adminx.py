# -*- coding: utf-8 -*-
__author__ = 'shine_forever'
__date__ = '2017/1/31 22:49'

from .models import Course,Lesson,Video,CourseResource

import xadmin

class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree','learn_times','students','fav_nums','image','click_nums','add_time']
    search_fields = ['name', 'desc', 'detail', 'degree','learn_times','students','fav_nums','image','click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree','learn_times','students','fav_nums','image','click_nums','add_time']
    model_icon = 'fa fa-user'  # 自定义icon，查看网站 http://fontawesome.io/
    ordering = ['-click_nums']   #按指定字段排序
    readonly_fields = ['click_nums']    #指定字段后台管理只读
    exclude = ['fav_nums']  #在后台指定哪些字段不显示

class LessonAdmin(object):
    list_display = ['course','name','add_time']
    search_fields = ['course','name']
    list_filter = ['course__name','name','add_time']   #course 是外键，需要显示名称


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download','add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download','add_time']


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)

