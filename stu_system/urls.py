from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('',views.tologin),
    path('index/',views.login),
    path('toregister/',views.toregister),
    path('register/',views.register),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('dashboard/withdraw_course/<str:course_id>/', views.withdraw_course, name='withdraw_course'),
    path('dashboard/course_selection/', views.course_selection, name='course_selection'),
    path('dashboard/personal_info/', views.personal_info, name='personal_info'),
    path('dashboard/course_selection/submit_selection/', views.submit_selection, name='submit_selection'),
    path('dashboard/course_selection/submit_selection/confirm_selection/<str:course_id>/', views.confirm_selection, name='confirm_selection'),
    path('dashboard/course_selection/submit_selection/cancel_selection/', views.cancel_selection, name='cancel_selection'),
    path('dashboard/personal_info/upload_image/',views.upload_image,name='upload_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)