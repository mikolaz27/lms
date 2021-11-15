from django.contrib import admin
from django import forms

from .models import Student, Course, Teacher, Room, Color, UserProfile, \
    CustomUser


class RoomAdminForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

    def clean_location(self):
        if self.cleaned_data["location"] == "Kiev":
            raise forms.ValidationError("Should be Kyiv instead of Kiev")

        return self.cleaned_data["location"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    form = RoomAdminForm


class StudentAdmin(admin.StackedInline):
    model = Student
    extra = 1


class TeacherAdmin(admin.TabularInline):
    model = Teacher.course.through
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [StudentAdmin]


class UserProfileAdmin(admin.StackedInline):
    model = UserProfile
    extra = 0


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = [UserProfileAdmin]


admin.site.register(Teacher)
