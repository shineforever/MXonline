# -*- coding: utf-8 -*-
__author__ = 'shine_forever'
__date__ = '2017/1/31 22:05'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord,Banner,UserProfile

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = "后台管理系统"
    site_footer = "by SRE demo"
    menu_style = "accordion"    #xadmin菜单收起来


class UserProfileAdmin(object):
    list_display = ['nick_name', 'birday', 'gender', 'address','mobile','image']
    search_fields = ['nick_name', 'birday', 'gender', 'address','mobile','image']
    list_filter = ['nick_name', 'birday', 'gender', 'address','mobile','image']


class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']


# xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)
