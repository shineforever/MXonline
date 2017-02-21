# coding: utf-8
from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import CityDict,CourseOrg
from .forms import UserAskForm

# Create your views here.

class OrgView(View):
    """
    课程机构列表
    """
    def get(self,request):
        #所有课程机构
        all_orgs = CourseOrg.objects.all()
        #热门机构
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        #所有城市
        all_citys = CityDict.objects.all()

        #取出筛选的城市：
        city_id = request.GET.get('city','')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id)) #由于是外键，所有可以直接用city_id来查询；

        #类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        #排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')

        # 所有机构数量；
        org_nums = all_orgs.count()

        #对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_orgs, 1,request=request)

        orgs = p.page(page)

        return render(request,'org-list.html',{
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums':org_nums,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort
        })


class AddUserAskView(View):
    """
    用户咨询模块，ajax实现，返回json
    """
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}',content_type='application/json')


