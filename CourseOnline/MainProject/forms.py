from django import forms
from .models import Announcement
# from .models import Role
from .models import Assignment
from .models import CourseMaterial
from .models import Grade
from .models import StudentUploadFile
from .models import Syllabus
from .models import Assistant
from django.forms import ClearableFileInput

# from .models import Instructor
# from .models import Student
# from .models import Assistant


class LoginForm (forms.Form):
    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class AnnouncementForm (forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'content')


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('title', 'content', 'doc_file', 'due_date')


class CourseMaterialForm(forms.ModelForm):
    print("CourseMaterialForm")

    class Meta:
        model = CourseMaterial
        fields = ('title', 'doc_file')


class GradeForm(forms.ModelForm):
    print("GradeForm")

    class Meta:
        model = Grade
        fields = ('title', 'doc_file')


class StudentUploadFileForm(forms.ModelForm):

    class Meta:
        model = StudentUploadFile
        fields = ('doc_file', )


class SyllabusForm(forms.ModelForm):

    class Meta:
        model = Syllabus
        fields = ('doc_file', )


# class AssistantForm(forms.ModelForm):
#     class Meta:
#         model = Assistant
#         fields = ('assistant_id', )