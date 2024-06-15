from django.urls import path

from . import views
urlpatterns = [
    path('',views.toLogin),
    path('index/', views.login),
    path('dashboard/', views.dashboard),
    path('student/', views.student_management,name='student_management'),
    path('student/edit_student/<str:student_id>/', views.edit_student,name='edit_student'),
    path('student/delete_student/<str:student_id>/', views.delete_student,name='delete_student'),
]