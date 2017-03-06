# coding: utf-8
from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import CityDict,CourseOrg,Teacher,CourseOrg
from .forms import UserAskForm
from operation.models import UserFavorite
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
        has_fav = False
        if request.user.is_authenticated():  #判断用户是否登录
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]  #通过机构名称反查出该机构下所有课程，使用set方法（外键）
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })

class OrgCourseView(View):
    """
    机构课程
    """
    def get(self,request,course_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(course_id))
        has_fav = False
        if request.user.is_authenticated():  # 判断用户是否登录
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        return render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page': current_page,
            'has_fav':has_fav
        })


class OrgDescView(View):
    """
    机构介绍页面
    """
    def get(self,request,course_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(course_id))
        has_fav = False
        if request.user.is_authenticated():  # 判断用户是否登录
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-desc.html',{
            'course_org':course_org,
            'current_page': current_page,
            'has_fav':has_fav
        })


class OrgTeacherView(View):
    """
    机构老师
    """
    def get(self,request,course_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(course_id))
        has_fav = False
        if request.user.is_authenticated():  # 判断用户是否登录
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=3):
                has_fav = True
        all_teachers = course_org.teacher_set.all()
        return render(request,'org-detail-teachers.html',{
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page': current_page,
            'has_fav':has_fav
        })

class AddFavView(View):
    """
    用户收藏
    1）判断用户是否登录
    2）fav_id传上来以后查看该用户是否收藏过，没有收藏就是收藏该项目，如果已经收藏，就取消收藏；
    """
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)  #如果默认是空字符串，int的时候会异常，所以默认值为0，记住获取的值为string类型，数据库查询的时候要转换为int
        fav_type = request.POST.get('fav_type',0)

        if not request.user.is_authenticated():  #判断用户是否登录
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        exists_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exists_records:
            #记录存在，则权限该收藏
            exists_records.delete()
            return HttpResponse('{"status":"fail","msg":"取消收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏失败"}', content_type='application/json')

class TeacherListView(View):
    """
    课程讲师列表页
    """
    def get(self,request):
        all_teachers = Teacher.objects.all()

        # 讲师人气排行
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')

        #讲师排行榜
        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:2]

        # 对课程讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_teachers, 1, request=request)
        teachers = p.page(page)

        return render(request,'teachers-list.html',{
            'all_teachers':teachers,
            'sorted_teachers':sorted_teachers,
            'sort':sort

        })

class TeacherDetailView(View):
    """
    讲师详情页
    """

    def get(self, request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher_courses = Course.objects.filter(teacher=teacher)

        # 讲师排行榜
        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:3]

        #讲师机构
        teacher_org = CourseOrg.objects.get(teacher=teacher)

        has_teacher_fav = False
        if UserFavorite.objects.filter(user=request.user,fav_type=3,fav_id=teacher.id):
            has_teacher_fav=True

        has_org_fav = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2,fav_id=teacher_org.id):
            has_org_fav = True

        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'teacher_courses':teacher_courses,
            'sorted_teachers':sorted_teachers,
            'teacher_org':teacher_org,
            'has_teacher_fav':has_teacher_fav,
            'has_org_fav':has_org_fav
        })


