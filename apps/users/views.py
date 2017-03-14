# coding: utf-8

import json

from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password  #密码加密函数

from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UploadImageForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.

class CustomBackend(ModelBackend):
    """
    自定义认证模块
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            # 因为密码为加密的，所以不能直接传入密码，要使用方法check_password
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class ActiveUserView(View):
    """
    邮件激活码
    """
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        # print all_records
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request,'active_fail.html')
        return render(request,"login.html")

class LoginView(View):
    def get(self,request):
        return render(request,"login.html")

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {"msg": "用户未激活！"})
            else:
                return render(request, 'login.html', {"msg": "用户或者密码错误！"})
        else:
            return render(request, 'login.html', {"login_form":login_form})


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,"register.html",{"register_form":register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"msg": "用户已存在","register_form":register_form})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(user_name,"register")
            return render(request, 'login.html')
        else:
            return render(request,"register.html",{"register_form":register_form})


class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html',{"forget_form":forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')
            send_register_email(email, "forget")
            return render(request,'send_success.html')
        else:
            return render(request,'forgetpwd.html',{"forget_form":forget_form})


class ResetView(View):
    """
    密码重置
    """

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        # print all_records
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,'password_reset.html',{'email':email})
        else:
            return render(request, 'active_fail.html')
        return render(request, "login.html")


class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pass1 = request.POST.get('password1','')
            pass2 = request.POST.get('password2','')
            email = request.POST.get('email','')
            if pass1 != pass2:
                return render(request,'password_reset.html',{'email':email,'msg':u'密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pass1)
            user.save()
            return render(request,'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


#
# def user_login(request):
#     """
#     用户登录
#     :param request:
#     :return:
#     """
#     if request.method == 'POST':
#         user_name = request.POST.get('username','')
#         pass_word = request.POST.get('password','')
#         user = authenticate(username=user_name,password=pass_word)
#         if user is not None:
#             login(request,user)
#             return render(request,'index.html')
#         else:
#             return render(request,'login.html',{"msg":"用户或者密码错误！"})
#     elif request.method == 'GET':
#         return render(request,'login.html')


class UserInfoView(LoginRequiredMixin,View):
    """
    用户信息，需要登录才可查看
    """
    def get(self,request):
        return render(request,'usercenter-info.html','')

class UploadImageView(LoginRequiredMixin,View):
    """
    用户图像上传
    """
    #方式一
    # def post(self,request):
    #     image_form = UploadImageForm(request.POST,request.FILES)  #文件上传要使用request.FILES
    #     if image_form.is_valid():
    #         image = image_form.cleaned_data['image']
    #         request.user.image = image
    #         request.user.save()
    #        pass

    #方式二 利用modeform功能 save
    def post(self,request):
        image_form = UploadImageForm(request.POST, request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin,View):
    """
    个人中心里面修改密码
    """
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pass1 = request.POST.get('password1','')
            pass2 = request.POST.get('password2','')
            if pass1 != pass2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pass1)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin,View):
    """
    发送邮箱的验证码
    """
    def get(self,request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        send_register_email(email,'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    """
    用户修改密码，验证流程
    """
    def post(self,request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')
