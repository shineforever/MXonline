# coding: utf-8

from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    """
    用户属性
    """
    nick_name = models.CharField(max_length=50,verbose_name=u'昵称',default=u'')
    birday = models.DateField(verbose_name=u'生日',null=True,blank=True)
    gender = models.CharField(choices=(('male',u'男'),('female',u'女')),default='female',max_length=6)
    address = models.CharField(max_length=100,verbose_name=u'地址',default=u'')
    mobile = models.CharField(max_length=11,null=True,blank=True)
    image = models.ImageField(upload_to="image/%Y/%m",default=u"image/default.png",max_length=100)

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    def get_unread_nums(self):
        """
        获取用户未读消息的个数
        :return:
        """
        from operation.models import UserMessage   #不放在全局，是怕循环import
        return UserMessage.objects.filter(user=self.id).count()


class EmailVerifyRecord(models.Model):
    """
    邮箱验证码
    """
    code = models.CharField(max_length=20,verbose_name=u'验证码')
    email = models.EmailField(max_length=50,verbose_name=u'邮箱')
    send_type = models.CharField(choices=(("register",u'注册'),('forget',u'忘记密码'),('update_email',u'修改邮箱')),default='register',max_length=20,verbose_name=u'验证码类型')
    send_time = models.DateTimeField(default=datetime.now,verbose_name=u'发送时间')

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        # return "%s(%s)" %(self.code,self.email)
        return '{0}({1})'.format(self.code,self.email)


class Banner(models.Model):
    """
    轮播图
    """
    title = models.CharField(max_length=100,verbose_name=u'标题')
    image = models.ImageField(upload_to='banner/%Y/%m',verbose_name=u'轮播图',max_length=100)
    url = models.URLField(max_length=200,verbose_name=u'访问地址')
    index = models.IntegerField(default=100,verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name

