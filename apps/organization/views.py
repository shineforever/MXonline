# coding: utf-8
from django.shortcuts import render
from django.views.generic import View

from .models import CityDict,CourseOrg

# Create your views here.

class OrgView(View):
    """
    课程机构列表
    """
    def get(self,request):
        #所有课程机构
        all_orgs = CourseOrg.objects.all()
        #所有机构数量；
        org_nums= all_orgs.count()
        #所有城市
        all_citys = CityDict.objects.all()
        return render(request,'org-list.html',{
            'all_orgs':all_orgs,
            'all_citys':all_citys,
            'org_nums':org_nums
        })
