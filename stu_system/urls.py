from django.urls import path

from . import views
urlpatterns = [
    path('',views.tologin),
    path('index/',views.login),
    path('toregister/',views.toregister),
    path('register/',views.register),
]