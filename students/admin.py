from django.utils.html import format_html
from django.contrib import admin
from django import forms

from .models import Student, Course, Teacher, Room, Color, UserProfile, \
    CustomUser


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'age', 'birthdate']
    search_fields = ['first_name__startswith', 'last_name__icontains']
    list_filter = ['first_name']

    # ordering = ['-birthdate']
    # Student.objects.filter(first_name__in=[''])


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'count_of_students']
    ordering = ['count_of_students']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email',
                    'course_count', 'list_courses']
    fieldsets = (
        ("Personal info", {
            'fields': ('first_name', 'last_name',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('email', 'phone_number'),
        }),
    )

    # fieldsets = (
    #     ("Personal info", {'fields': ['first_name', 'last_name']})
    # )

    def list_courses(self, obj):
        if obj.course:
            courses = obj.course.all()
            # students/course/e93b7cc6-5d55-44a7-91cf-0bcafaa3bbc2/change/
            # {reverse('admin:students_course_change', args=course.pk)}
            links = [
                f"<a href='http://127.0.0.1:8000/admin/students/course/{course.pk}/change/'>{course.name}</p>"
                for course in courses]

            return format_html(f"{''.join(links)}")
        else:
            return format_html("Empty courses")

    def course_count(self, obj):
        if obj.course:
            courses = obj.course.all().count()
            return format_html(f"<p>{courses}</p>")
        else:
            return format_html(f"<p>0</p>")


# class RoomAdminForm(forms.ModelForm):
#     class Meta:
#         model = Room
#         fields = '__all__'
#
#     def clean_location(self):
#         if self.cleaned_data["location"] == "Kiev":
#             raise forms.ValidationError("Should be Kyiv instead of Kiev")
#
#         return self.cleaned_data["location"]
#
#
# @admin.register(Room)
# class RoomAdmin(admin.ModelAdmin):
#     form = RoomAdminForm
#
#
# class StudentAdmin(admin.StackedInline):
#     model = Student
#     extra = 1
#
#
# class TeacherAdmin(admin.TabularInline):
#     model = Teacher.course.through
#     extra = 1
#
#
# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     inlines = [StudentAdmin]
#
#
# class UserProfileAdmin(admin.StackedInline):
#     model = UserProfile
#     extra = 0
#
#
# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
#     inlines = [UserProfileAdmin]



# admin.site.register(Student, StudentAdmin)
admin.site.register(UserProfile)
# admin.site.register(Teacher)
admin.site.register(Room)
admin.site.register(Color)
admin.site.register(CustomUser)
