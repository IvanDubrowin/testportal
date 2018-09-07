from django.urls import path
from django.conf.urls import include
from django.views.generic import ListView
from portal.models import Course, Question
from portal import views


urlpatterns = [
        path('', ListView.as_view(queryset=Course.objects.all(), template_name="index.html"), name='index'),
        path('stat/', views.StatisticView.as_view(), name='statistic'),
        path('<int:pk>/', views.CourseView.as_view(), name='course'),
        path('register', views.RegisterFormView.as_view(), name='register')
]
