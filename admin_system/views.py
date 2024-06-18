from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.http import HttpResponse
from django.urls import reverse
from django.db import connection
import time
# Create your views here.

def toLogin(request):
    return render(request, 'admin_system/login.html')

def login(request):

    u = request.POST.get("user","")
    p = request.POST.get("pwd","")
    print(u, p)
    if u and p:
        c = Adminsystemaccount.objects.filter(admin_user=u,admin_password=p).count()
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
        student.enrollment_data = enrollment_data
        student.major = major
        student.awards_and_punishments = awards_and_punishments
        student.save()
        redirect_url = reverse('student_management')
        return redirect(redirect_url)
    return render(request,'admin_system/edit_student.html',{'student':student})
def delete_student(request,student_id):
    with connection.cursor() as cursor:
        cursor.callproc("delete_student_with_course", [student_id])
    redirect_url = reverse('student_management')
    return redirect(redirect_url)

def add_student(request):
    if request.method == 'POST':
        student_id = request.POST.get("student_id","")
        name = request.POST.get("name","")
        enrollment_data = request.POST.get("enrollment_date","")
        major = request.POST.get("major","")
        awards_and_punishments = request.POST.get("awards_and_punishments","")
        try:
            if Students.objects.filter(student_id=student_id).exists():
                # Display error message
                messages.error(request, "学生ID已存在！")
            else:
                # Save the student record to the database
                student = Students(
                    student_id=student_id,
                    name=name,
                    enrollment_data=enrollment_data,
                    major=major,
                    awards_and_punishments=awards_and_punishments
                )
                student.save()
                # Redirect to the student list page or any other desired page
                redirect_url = reverse('student_management')
                return redirect(redirect_url)

        except Exception as e:
            # Display error message
            messages.error(request, "学生添加失败：" + str(e))
    return render(request,'admin_system/add_student.html')

def course_management(request):
    courses = Courses.objects.all()
    return render(request, 'admin_system/course.html', {'courses': courses})

def edit_course(request,course_id):
    course = Courses.objects.get(course_id=course_id)
    if request.method == 'POST':
        name = request.POST.get("name","")
        instructor = request.POST.get("instructor","")
        year_offered = request.POST.get("year_offered","")
        credits = request.POST.get("credits","")
        course.name = name
        course.instructor = instructor
        course.year_offered = year_offered
        course.credits = credits
        course.save()
        redirect_url = reverse('course_management')
        return redirect(redirect_url)
    return render(request,'admin_system/edit_course.html',{'course':course})

def delete_course(request,course_id):
    with connection.cursor() as cursor:
        cursor.callproc("delete_course_with_student", [course_id])
    redirect_url = reverse('course_management')
    return redirect(redirect_url)

def add_course(request):
    if request.method == 'POST':
        course_id = request.POST.get("course_id","")
        course_name = request.POST.get("name","")
        instructor = request.POST.get("instructor","")
        year_offered = request.POST.get("year_offered","")
        credits = request.POST.get("credits","")
        try:
            if Courses.objects.filter(course_id=course_id).exists():
                # Display error message
                messages.error(request, "课程ID已存在！")
            else:
                # Save the student record to the database
                course = Courses(
                    course_id=course_id,
                    course_name=course_name,
                    instructor=instructor,
                    year_offered=year_offered,
                    credits=credits
                )
                course.save()
                # Redirect to the student list page or any other desired page
                redirect_url = reverse('course_management')
                return redirect(redirect_url)

        except Exception as e:
            # Display error message
            messages.error(request, "课程添加失败：" + str(e))
    return render(request,'admin_system/add_course.html')

def enrollment_management(request):
    enrollments = Enrollments.objects.all()
    return render(request,'admin_system/enrollment.html',{'enrollments':enrollments})

def edit_enrollment(request,student_id,course_id):
    enrollment = Enrollments.objects.get(student_id=student_id,course_id=course_id)
    if request.method == 'POST':
        grade = request.POST.get("grade","")
        with connection.cursor() as cursor:
            cursor.callproc('edit_grade', [student_id, course_id, grade])
        redirect_url = reverse('enrollment_management')
        return redirect(redirect_url)
    return render(request,'admin_system/edit_enrollment.html',{'enrollment':enrollment})

def delete_enrollment(request,student_id,course_id):
    with connection.cursor() as cursor:
        cursor.callproc('delete_enrollment', [student_id,course_id])
    redirect_url = reverse('enrollment_management')
    return redirect(redirect_url)

def add_enrollment(request):
    if request.method == 'POST':
        course_id = request.POST.get("course_id")
        student_id = request.POST.get("student_id")
        grade = request.POST.get("grade")
        if not course_id or not student_id:
            messages.error(request, 'Course and student must be selected.')
        print("student_id:",student_id)
        try:

            if Enrollments.objects.filter(student_id=student_id,course_id=course_id).exists():
                # Display error message
                messages.error(request, "选课信息已存在！")
            else:
                # Save the student record to the database
                if not isinstance(student_id, str):
                    print("非字符串！")
                print("ok")
                print(student_id)
                with connection.cursor() as cursor:
                    cursor.callproc('insert_enrollment', [student_id, course_id, grade])
                # Redirect to the student list page or any other desired page
                redirect_url = reverse('enrollment_management')
                return redirect(redirect_url)

        except Exception as e:
            # Display error message
            messages.error(request, "选课信息添加失败：" + str(e))
    students = Students.objects.all()
    courses = Courses.objects.all()
    context = {'students':students,'courses':courses}
    return render(request,'admin_system/add_enrollment.html',context)