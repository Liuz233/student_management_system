from django.shortcuts import render,redirect

from .models import *
from django.http import HttpResponse
from django.urls import reverse
# Create your views here.
def toLogin(request):
    return render(request, 'admin_system/login.html')

def login(request):

    u = request.POST.get("user","")
    p = request.POST.get("pwd","")
    print(u, p)
    if u and p:
        c = AdminSystemAccount.objects.filter(admin_user=u,admin_password=p).count()
        if c > 0:
            return render(request,'admin_system/login_success.html')
        else:
            return render(request,'admin_system/login_fail.html')
    else:
        return render(request,'admin_system/login_fail.html')
def dashboard(request):
    return render(request,'admin_system/dashboard.html')

def student_management(request):
    students = Students.objects.all()
    return render(request, 'admin_system/student.html', {'students': students})

def edit_student(request,student_id):
    student = Students.objects.get(student_id=student_id)
    if request.method == 'POST':
        name = request.POST.get("name","")
        enrollment_data = request.POST.get("enrollment_date","")
        major = request.POST.get("major","")
        awards_and_punishments = request.POST.get("awards_and_punishments","")
        student.name = name
        student.enrollment_date = enrollment_data
        student.major = major
        student.awards_and_punishments = awards_and_punishments
        student.save()
        redirect_url = reverse('student_management')
        return redirect(redirect_url)
    return render(request,'admin_system/edit_student.html',{'student':student})
def delete_student(request,student_id):
    return HttpResponse("ok")