"""lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from students.views import (
    hello,
    get_students,
    # create_student,
    update_student,
    delete_student,
    create_teacher,
    test_view,
    search_view, CreateStudent, UpdateStudent, LoginStudent,
    RegistrationStudent, LogoutStudent, send_email
)

app_name = "students"

urlpatterns = [
    path("", get_students, name="list"),
    path("create/", CreateStudent.as_view(), name="create"),
    path("update/<int:pik>/", UpdateStudent.as_view(), name="update"),
    path("create-teacher/", create_teacher, name="create-teacher"),
    path("delete/<int:pk>/", delete_student, name="delete"),
    path("test/", test_view, name="test"),
    path("search/", search_view, name="search"),
    path("login/", LoginStudent.as_view(), name="login"),
    path("logout/", LogoutStudent.as_view(), name="logout"),
    path("registration/", RegistrationStudent.as_view(), name="registration"),
    path('send_email/', send_email, name='send_email')
]
