# coding: utf-8

from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password  #密码加密函数

from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm
from utils.email_send import send_register_email

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
        all_records = EmailVerifyRecord.objects.filter(active_code)
        # print all_records
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
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