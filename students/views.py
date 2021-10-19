from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from webargs import fields

from students.forms import StudentCreateForm, TeacherBaseForm
from students.models import Student
from students.utils import format_records
from django.core.exceptions import BadRequest
from webargs import djangoparser
from django.contrib.auth.models import User


def hello(request):
    return HttpResponse("SUCCESS")


def index(request):
    return render(
        request=request,
        template_name="index.html",
    )


parser = djangoparser.DjangoParser()


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)


@parser.use_args(
    {
        "first_name": fields.Str(
            required=False,
        ),
        "text": fields.Str(required=False),
    },
    location="query",
)
def get_students(request, params):
    students = Student.objects.all().order_by("-id")

    text_fields = ["first_name", "last_name", "email"]

    for param_name, param_value in params.items():
        if param_value:
            if param_name == "text":
                or_filter = Q()
                for field in text_fields:
                    or_filter |= Q(**{f"{field}__contains": param_value})
                students = students.filter(or_filter)
            else:
                students = students.filter(**{param_name: param_value})

    return render(
        request=request,
        template_name="students_table.html",
        context={"students_list": students}
    )


@csrf_exempt
def create_student(request):
    if request.method == "POST":
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("students:list"))

    elif request.method == "GET":
        form = StudentCreateForm()

    return render(
        request=request,
        template_name="students_create.html",
        context={"form": form}
    )


@csrf_exempt
def create_teacher(request):
    if request.method == "POST":
        form = TeacherBaseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("students:list"))

    elif request.method == "GET":
        form = TeacherBaseForm()

    return render(
        request=request,
        template_name="teacher_create.html",
        context={"form": form}
    )


def delete_student(request, pk):
    student = get_object_or_404(Student, id=pk)
    student.delete()

    return HttpResponseRedirect(reverse("students:list"))


@csrf_exempt
def update_student(request, pk):
    student = get_object_or_404(Student, id=pk)

    if request.method == "POST":
        form = StudentCreateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("students:list"))

    elif request.method == "GET":
        form = StudentCreateForm(instance=student)

    form_html = f"""
    <form method="POST">
      {form.as_p()}
      <input type="submit" value="Save">
    </form>
    """

    return HttpResponse(form_html)
