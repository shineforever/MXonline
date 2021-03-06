# -*- coding: utf-8 -*-
__author__ = 'shine_forever'
__date__ = '2017/1/31 23:20'

from .models import CityDict,CourseOrg,Teacher

import xadmin

class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc','click_nums','fav_nums','image','address','city','add_time']
    search_fields = ['name', 'desc','click_nums','fav_nums','image','address','city__name']
    list_filter = ['name', 'desc','click_nums','fav_nums','image','address','city','add_time']
    relfield_style = 'fk-ajax'   #以ajax方式加载外键


class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_years','work_company','work_position','points','click_nums','fav_nums','add_time']
    search_fields = ['name', 'org', 'work_years','work_company','work_position','points','click_nums','fav_nums']
    list_filter = ['name', 'org', 'work_years','work_company','work_position','points','click_nums','fav_nums','add_time']


xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
