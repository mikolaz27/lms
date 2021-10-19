from django.contrib import admin
from .models import Student, Course, Teacher

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Teacher)