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
            return render(request,'login_fail.html')
    else:
        return render(request,'login_fail.html')
def toregister(request):
    return render(request,'register.html')

def register(request):
    u = request.POST.get("user","")
    p = request.POST.get("pwd","")
    if u and p:
        stu = StuSystemStudentaccount(student_id=u , stu_password=p)
        stu.save()
        return render(request,'register_success.html')
    else:
        return HttpResponse("请输入完整账号及密码！")
