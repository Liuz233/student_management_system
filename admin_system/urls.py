from django.urls import path

from . import views
urlpatterns = [
    path('',views.toLogin),
    path('index/', views.login),
    path('dashboard/', views.dashboard),
    path('student/', views.student_management,name='student_management'),
    path('student/edit_student/<str:student_id>/', views.edit_student,name='edit_student'),
    path('student/delete_student/<str:student_id>/', views.delete_student,name='delete_student'),
    path('student/add_student/', views.add_student,name='add_student'),
    path('course/', views.course_management,name='course_management'),
    path('course/edit_course/<str:course_id>/', views.edit_course, name='edit_course'),
    path('course/delete_course/<str:course_id>/', views.delete_course, name='delete_course'),
    path('course/add_course/', views.add_course,name='add_course'),
    path('enrollment/', views.enrollment_management,name='enrollment_management'),
    path('enrollment/edit_enrollment/<str:student_id>/<str:course_id>/', views.edit_enrollment, name='edit_enrollment'),
    path('enrollment/delete_enrollment/<str:student_id>/<str:course_id>/', views.delete_enrollment, name='delete_enrollment'),
    path('enrollment/add_enrollment/', views.add_enrollment, name='add_enrollment'),
]