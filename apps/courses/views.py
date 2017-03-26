# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import Course,CourseResource,Video
from operation.models import UserFavorite,CourseComments,UserCourse
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.

class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        search_keywords = request.GET.get('keywords','')
        #搜索框中课程搜索
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))

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

class CourseInfoView(LoginRequiredMixin,View):
    """
    课程章节信息
    """
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        #查询用户是否已经关联了课程
        user_courses =UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses: #判断用户是否学习了改课程，如果没有学习，就关联该课程
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)   #找出学过该课程的学生
        user_ids = [user_course.user.id for user_course in user_courses]  #找出学了该课程的用户id，组合成一个list
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  #传入用户的列表，得到该列表中所有用户课程id的list
        #取出所有课程的id
        course_ids = [user_course.course.id for user_course in user_courses]
        # 通过用户的课程id，找出相关课程，并且按照点击数，倒序排序
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'all_resources':all_resources,
            'relate_courses':relate_courses
        })

class CommentView(LoginRequiredMixin,View):
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

class VideoPlayView(View):
    """
    视频播放
    """
    def get(self,request,video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        #查询用户是否已经关联了课程
        user_courses =UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses: #判断用户是否学习了改课程，如果没有学习，就关联该课程
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)   #找出学过该课程的学生
        user_ids = [user_course.user.id for user_course in user_courses]  #找出学了该课程的用户id，组合成一个list
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  #传入用户的列表，得到该列表中所有用户课程id的list
        #取出所有课程的id
        course_ids = [user_course.course.id for user_course in user_courses]
        # 通过用户的课程id，找出相关课程，并且按照点击数，倒序排序
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'course': course,
            'all_resources':all_resources,
            'relate_courses':relate_courses,
            'video':video
        })

