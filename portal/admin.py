from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from .models import Course, Question, UserCourseStat


class MyAdminSite(AdminSite):
    site_header = 'TESTPORTAL Admin'

admin_site = MyAdminSite(name='admin')
admin_site.register([Course, Question, UserCourseStat, User])
