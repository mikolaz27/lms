from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from webargs import fields

from students.forms import StudentCreateForm
from students.models import Student
from students.utils import format_records
from django.core.exceptions import BadRequest
from webargs import djangoparser


def hello(request):
    return HttpResponse('SUCCESS')


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

    form = """
    <form >
      <label>First name:</label><br>
      <input type="text" name="first_name"><br>
      
      <label>Text:</label><br>
      <input type="text" name="text" placeholder="Enter text to search"><br><br>
    
      <input type="submit" value="Search">
    </form>
    """

    students = Student.objects.all().order_by('-id')

    text_fields = ['first_name', 'last_name', 'email']

    for param_name, param_value in params.items():
        if param_value:
            if param_name == 'text':
                or_filter = Q()
                for field in text_fields:
                    or_filter |= Q(**{f'{field}__contains': param_value})
                students = students.filter(or_filter)
            else:
                students = students.filter(**{param_name: param_value})

    result = format_records(students)

    response = form + result

    return HttpResponse(response)


@csrf_exempt
def create_student(request):

    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('students-list'))

    elif request.method == 'GET':
        form = StudentCreateForm()

    form_html = f"""
    <form method="POST">
      {form.as_p()}
      <input type="submit" value="Create">
    </form>
    """

    return HttpResponse(form_html)


@csrf_exempt
def update_student(request, pk):

    student = get_object_or_404(Student, id=pk)

    if request.method == 'POST':
        form = StudentCreateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('students-list'))

    elif request.method == 'GET':
        form = StudentCreateForm(instance=student)

    form_html = f"""
    <form method="POST">
      {form.as_p()}
      <input type="submit" value="Save">
    </form>
    """

    return HttpResponse(form_html)
