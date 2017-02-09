# coding: utf-8

from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View

from .models import UserProfile
from .forms import LoginForm
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
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {"msg": "用户或者密码错误！"})
        else:
            return render(request, 'login.html', {"login_form":login_form})


class RegisterView(View):
    def get(self,request):
        return render(request,"register.html")


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