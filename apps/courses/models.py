# coding: utf-8

from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from organization.models import CourseOrg,Teacher

# Create your models here.


class Course(models.Model):
    """
    课程
    """
    name = models.CharField(max_length=50,verbose_name=u'课程名称')
    course_org = models.ForeignKey(CourseOrg,verbose_name=u"课程机构",null=True,blank=True)
    desc = models.CharField(max_length=300,verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    teacher = models.ForeignKey(Teacher,verbose_name=u'授课老师',null=True,blank=True)  #为什么这个地方不是有default，因为这个是外键，定义了默认值，只能是允许为空
    degree = models.CharField(choices=(('cj',u'初级'),('zj',u'中级'),('gj',u'高级')),max_length=2,verbose_name=u'难度等级')
    learn_times = models.IntegerField(default=0,verbose_name=u'学习时长(分钟数)')
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏次数')
    image = models.ImageField(upload_to='courses/%Y/%m',verbose_name=u'封面图',max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name=u'点击数')
    category = models.CharField(max_length=300,default=u'后端开发',verbose_name=u'课程类别')
    tag = models.CharField(max_length=100,default='',verbose_name=u'课程标签')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    youneed_know = models.CharField(max_length=300,default='',verbose_name=u'课程须知')
    teacher_tell = models.CharField(max_length=300,default='',verbose_name=u'老师告诉你')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        """
        获取章节数量（自定义）
        :return:
        """
        return self.lesson_set.all().count()

    def get_learn_nums(self):
        """
        获得学习该课程的人数,取前5（通过外键来反查）
        :return:
        """
        return self.usercourse_set.all()[:5]

    def get_learn_users(self):
        """
        获得学习学生
        :return:
        """
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        """
        获得课程的章节数
        """
        return self.lesson_set.all()

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    """
    章节
    """
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=100,verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_video(self):
        """
        获得章节下面有哪些视频
        :return:
        """
        return self.video_set.all()

class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名称')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    url = models.CharField(max_length=200, default='', verbose_name=u"访问地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'课程资源')
    download = models.FileField(upload_to='course/resource/%Y/%m',verbose_name=u'资源文件',max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name