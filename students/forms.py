from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, EmailField
from students.models import Student, Teacher, CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationStudentForm(UserCreationForm):
    email = EmailField(max_length=200,
                       help_text="Registration without email is not possible!")

    class Meta:
        model = CustomUser
        fields = [ 'email', 'password1', 'password2']


class PersonBaseForm(ModelForm):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "email", "phone_number", "course"]

    @staticmethod
    def normalize_name(name):
        return name.lower().strip().capitalize()

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]

        return self.normalize_name(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]

        return self.normalize_name(last_name)

    def clean(self):
        cleaned_data = super().clean()

        first_name = cleaned_data["first_name"]
        last_name = cleaned_data["last_name"]
        if first_name == last_name:
            raise ValidationError("First and last names can't be equal")

        return cleaned_data


class StudentCreateForm(PersonBaseForm):
    pass


class StudentUpdateForm(PersonBaseForm):
    class Meta(PersonBaseForm.Meta):
        fields = ["first_name", "last_name", "email", "phone_number",
                  "birthdate"]


class TeacherBaseForm(PersonBaseForm):
    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "email", "phone_number", "course"]

        widgets = {
            "phone_number": TextInput(
                attrs={"pattern": "\d{10,14}", "label": ""})
        }
