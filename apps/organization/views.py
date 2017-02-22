# coding: utf-8
from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import CityDict,CourseOrg
from .forms import UserAskForm
from courses.models import Course

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


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self,request,org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]  #通过机构名称反查出该机构下所有课程，使用set方法（外键）
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page
        })

class OrgCourseView(View):
    """
    机构课程
    """
    def get(self,request,course_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(course_id))
        all_courses = course_org.course_set.all()
        return render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page': current_page
        })


class OrgDescView(View):
    """
    机构介绍页面
    """
    def get(self,request,course_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(course_id))
        return render(request,'org-detail-desc.html',{
            'course_org':course_org,
            'current_page': current_page
        })


class OrgTeacherView(View):
    """
    机构老师
    """
    def get(self,request,course_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(course_id))
        all_teachers = course_org.teacher_set.all()
        return render(request,'org-detail-teachers.html',{
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page': current_page
        })