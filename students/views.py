from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.forms.utils import ErrorList
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from webargs import fields

from students.forms import StudentCreateForm, TeacherBaseForm, \
    RegistrationStudentForm
from students.models import *
from students.utils import format_records
from django.core.exceptions import BadRequest, ValidationError
from webargs import djangoparser
from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, UpdateView
from django.core.mail import send_mail, EmailMessage


class IndexPage(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    login_url = reverse_lazy('students:login')
    extra_context = {'name': 'Mykhailo'}
    # http_method_names = ["post"]
    # def get(self, ):
    # def dispatch(self, request, *args, **kwargs):


def hello(request):
    return HttpResponse("SUCCESS")


#
# def index(request):
#     return render(
#         request=request,
#         template_name="index.html",
#     )


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
        context={"students_list": students},
    )


class CreateStudent(CreateView):
    # form_class = StudentCreateForm
    template_name = "students_create.html"
    fields = "__all__"
    model = Student
    initial = {
        "first_name": "default",
        "last_name": "default",
    }
    success_url = reverse_lazy("students:list")

    #
    # def get_success_url(self):
    #     return reverse("students:list")
    def form_valid(self, form):
        self.object = form.save(commit=False)
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        if first_name == last_name:
            form._errors["first_name"] = ErrorList(["dsadas"])
            form._errors["last_name"] = ErrorList(
                [u"You already have an email with that name man."])
            return super().form_invalid(form)
        return super().form_valid(form)


# def create_student(request):
#     print(request.session.get("last_search_text"))
#     if request.method == "POST":
#         form = StudentCreateForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("students:list"))
#
#     elif request.method == "GET":
#         form = StudentCreateForm()
#
#     return render(
#         request=request, template_name="students_create.html",
#         context={"form": form}
#     )


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
        request=request, template_name="teacher_create.html",
        context={"form": form}
    )


def delete_student(request, pk):
    student = get_object_or_404(Student, id=pk)
    student.delete()

    return HttpResponseRedirect(reverse("students:list"))


class UpdateStudent(UpdateView):
    model = Student
    template_name = "students_update.html"
    fields = "__all__"
    success_url = reverse_lazy("students:list")


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


def test_view(request):
    # 1.
    # my_student_1 = Course.objects.first()
    # course = Course.objects.get(id="482fdb3c-3a7f-4750-913a-65a8b091a7ab")
    # print(type(my_student.course))
    # print(type(my_student_1.course))
    # print(type(my_student.course))
    # print(course.)
    # students = Student.objects.filter(course__name__contains="In")
    # print(Student.objects.filter(course=))
    # print(Student.objects)
    # print(type(course.students))

    # for i in range(100):
    #     new_color = Color()
    #     new_color.name = "red"
    #     new_color.save()

    data_to_save = []
    course = Course.objects.get(id="482fdb3c-3a7f-4750-913a-65a8b091a7ab")

    for i in range(1000):
        new_student = Student()
        new_student.first_name = "12"
        new_student.last_name = "12"
        new_student.email = "test"
        new_student.course = course
        data_to_save.append(new_student)
        # new_color.save()

    Student.objects.bulk_create(data_to_save)

    student = Student.objects.filter(course__room__color__name__contains="red")

    return HttpResponse(student)


def search_view(request):
    search_text = request.GET.get('search')
    text_fields = ["first_name", "last_name", "email"]
    request.session["last_search_text"] = search_text
    print(request.GET)

    if search_text:
        or_filter = Q()
        for field in text_fields:
            or_filter |= Q(**{f"{field}__icontains": search_text})
        students = Student.objects.filter(or_filter)
    else:
        students = Student.objects.all().order_by("-id")

    return render(
        request=request,
        template_name="students_table.html",
        context={"students_list": students},
    )


class LoginStudent(LoginView):
    pass


class LogoutStudent(LogoutView):
    template_name = 'registration/logged_out.html'


class RegistrationStudent(CreateView):
    form_class = RegistrationStudentForm
    template_name = "registration/registration.html"
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        return super().form_valid(form)


def send_email(request):
    email = EmailMessage(subject='Registration from LMS',
                         body="Test text",
                         to=['alexfoxalt@gmail.com'])
    email.send()
    return HttpResponse('Done')
