# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import Course,CourseResource
from operation.models import UserFavorite,CourseComments

# Create your views here.

class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        # 排序
        sort = request.GET.get('sort', '')  #获得get请求中url里面的sort参数值；
        if sort == 'students':
            all_courses = all_courses.order_by('-students')
        elif sort == 'hot':
            all_courses = all_courses.order_by('-click_nums')

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)
        return render(request,'course-list.html',{
            'all_courses':courses,
            'sort':sort,
            'hot_courses':hot_courses
        })

class CourseDetailView(View):
    """
    课程详情
    """
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save() #课程点击数

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():  #判断用户是否登录
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user,fav_id=course.course_org.id,fav_type=2):
                has_fav_org = True

        tag = course.tag
        #如果存在相关课程的tag，就推荐相关的tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            relate_courses = []   #如果没有推荐的课程，参数也应该为一个list，要不然模板里面for循环就会报错！

        return render(request,'course-detail.html',{
            'course':course,
            'relate_courses':relate_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org
        })

class CourseInfoView(View):
    """
    课程章节信息
    """
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'all_resources':all_resources
        })

class CommentView(View):
    """
    课程评论
    """
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()

        return render(request,'course-comment.html',{
            'course':course,
            'all_resources':all_resources,
            'all_comments':all_comments
        })

class AddCommentsView(View):
    """
    用户添加评论
    """
    def post(self,request):
        if not request.user.is_authenticated():  #判断用户是否登录
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()

            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')

