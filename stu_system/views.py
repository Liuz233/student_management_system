from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def tologin(request):
    return render(request,'login.html')

def login(request):
    u = request.POST.get("user","")
    p = request.POST.get("pwd","")

    if u and p:
        c = StuSystemStudentaccount.objects.filter(student_id=u , stu_password=p).count()
        if c > 0:
            return render(request,'login_success.html')
        else:
            return HttpResponse("账号或密码错误!")
    else:
        return HttpResponse("登录失败!")
def toregister(request):
    return render(request,'register.html')

def register(request):
    u = request.POST.get("user","")
    p = request.POST.get("pwd","")
    if u and p:
        stu = StuSystemStudentaccount(student_id=u , stu_password=p)
        stu.save()
        return HttpResponse("注册成功！")
    else:
        return HttpResponse("请输入完整账号及密码！")
