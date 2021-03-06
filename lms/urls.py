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
from django.conf import settings

from django.contrib import admin
from django.urls import path, include, re_path
from students.views import hello, get_students, update_student, IndexPage

urlpatterns = [
    path("", IndexPage.as_view(), name="index"),
    # path("index/", index),
    path("admin/", admin.site.urls),
    path("hello/", hello),
    path("students/", include("students.urls")),
    path('oauth/', include('social_django.urls'), name='social')
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path("__debug__/", include(debug_toolbar.urls)),
                  ] + urlpatterns
