from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.db.models import F
from django.urls import reverse
from django.db import connection
import os
# Create your views here.
def tologin(request):
    return render(request,'login.html')

def login(request):
    u = request.POST.get("user","")
    p = request.POST.get("pwd","")

    if u and p:
        c = StuSystemStudentaccount.objects.filter(student_id=u , stu_password=p).count()
        if c > 0:
            request.session['user'] = u
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
        c = Students.objects.filter(student_id=u).count()
        if c > 0:
            student = Students.objects.get(student_id=u)
            stu_name = student.name
            stu = StuSystemStudentaccount(student_id=u , stu_name=stu_name, stu_password=p)
            stu.save()
            return render(request,'register_success.html')
        else:
            return HttpResponse("学号不存在！")
    else:
        return HttpResponse("请输入完整账号及密码！")
def dashboard(request):
    u = request.session.get('user')
    student = Students.objects.get(student_id=u)
    enrollments = Enrollments.objects.filter(student_id=u).select_related('course')
    enrollments = enrollments.annotate(
        course_name=F('course__course_name'),
        instructor=F('course__instructor'),
        year_offered=F('course__year_offered'),
        credits=F('course__credits'),
    )
    context={
        'student': student,
        'enrollments': enrollments,
    }
    # for enrollment in enrollments:
    #     print("Student ID:", enrollment.student_id)
    #     print("Course ID:", enrollment.course_id)
    #     print("Grade:", enrollment.grade)
    #     print("GPA:", enrollment.gpa)
    #     print("Course Name:", enrollment.course.course_name)
    #     print("Instructor:", enrollment.course.instructor)
    #     print("Year Offered:", enrollment.course.year_offered)
    #     print("Credits:", enrollment.course.credits)
    #     print("---")
    return render(request,'dashboard.html',context)
def withdraw_course(request,course_id):
    student_id = request.session.get('user')
    with connection.cursor() as cursor:
        cursor.callproc('delete_enrollment', [student_id,course_id])
    redirect_url = reverse('dashboard')
    return redirect(redirect_url)
def course_selection(request):
    courses = Courses.objects.all()
    return render(request,'course_selection.html', {'courses':courses})
def submit_selection(request):

    course_id = request.POST.get('course_id')
    print('course_id:',course_id)
    course = Courses.objects.get(course_id=course_id)
    return render(request,'submit_selection.html',{'course':course})
def confirm_selection(request, course_id):
    student_id = request.session.get('user')
    c = Enrollments.objects.filter(course_id=course_id, student_id=student_id).count()
    if c > 0:
        return render(request, 'select_fail.html')
    else:
        grade = None
        with connection.cursor() as cursor:
            cursor.callproc('insert_enrollment', [student_id, course_id, grade])
        redirect_url = reverse('dashboard')
        return redirect(redirect_url)
def cancel_selection(request):
    redirect_url = reverse('dashboard')
    return redirect(redirect_url)
def personal_info(request):
    student_id = request.session.get('user')
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT calculate_weighted_gpa('{student_id}')")
        gpa_result = cursor.fetchone()
        weighted_gpa = gpa_result[0] if gpa_result else 0.0
    print('weighted_gpa:',weighted_gpa)
    context = {
        'weighted_gpa': weighted_gpa,
        'student_id': student_id,
    }
    return render(request,'personal_info.html',context)

from django.conf import settings


def upload_image(request):

    if request.method == 'POST' and request.FILES.get('image'):
        # 从会话中获取student_id
        student_id = request.session.get('user')

        # 构建保存图片的路径
        save_dir = os.path.join(settings.BASE_DIR, 'stu_system', 'static', 'images', str(student_id))
        os.makedirs(save_dir, exist_ok=True)

        image = request.FILES['image']
        image_path = os.path.join(save_dir, 'personal.jpg')

        with open(image_path, 'wb') as file:
            file.write(image.read())
    redirect_url = reverse('personal_info')
    return redirect(redirect_url)
