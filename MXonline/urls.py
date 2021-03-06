#coding: utf - 8

"""MXonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve

from users.views import LoginView,LogoutView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView,IndexView
from MXonline.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    # url(r'^$', TemplateView.as_view(template_name="index.html"),name="index"), #静态页面使用TemplateView
    #网站首页
    url(r'^$', IndexView.as_view(),name="index"),
    url(r'^login/$', LoginView.as_view(),name="login"),
    url(r'^logout/$', LogoutView.as_view(),name="logout"),
    url(r'^register/$', RegisterView.as_view(),name="register"),
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name="user_active"),
    url(r'^forget/$', ForgetPwdView.as_view(),name="forget_password"),
    url(r'^reset/(?P<active_code>.*)/$',ResetView.as_view(),name="reset_pwd"),
    url(r'^modifypwd/$', ModifyPwdView.as_view(),name="modify_pwd"),
    #课程机构
    url(r'^org/', include('organization.urls',namespace='org')),
    #课程相关
    url(r'^course/', include('courses.urls',namespace='course')),
    #用户中心相关
    url(r'^users/', include('users.urls',namespace='users')),
    #配置用户上传文件后的url处理函数；
    url(r'^media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),
]
