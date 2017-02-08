# coding: utf-8

from django.shortcuts import render

from django.contrib.auth import authenticate,login

# Create your views here.
def user_login(request):
    """
    用户登录
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_name = request.POST.get('username','')
        pass_word = request.POST.get('password','')
        user = authenticate(username=user_name,password=pass_word)
        if user is not None:
            login(request,user)
            return render(request,'index.html')
        else:
            return render(request,'login.html',{})
    elif request.method == 'GET':
        return render(request,'index.html')