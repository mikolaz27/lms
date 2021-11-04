from django.contrib import admin
from .models import Student, Course, Teacher, Room, Color, UserProfile


admin.site.register(Student)
admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Room)
admin.site.register(Color)
