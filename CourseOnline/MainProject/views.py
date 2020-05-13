from django.shortcuts import render
from django.utils import timezone
from .models import Announcement, Instructor, Assistant, Lecture, Student
from .models import Assignment, CourseMaterial, StudentUploadFile, Grade, Syllabus
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404, reverse
from django.contrib import messages
from .forms import AnnouncementForm, CourseMaterialForm, AssignmentForm
from .forms import GradeForm, StudentUploadFileForm, SyllabusForm
from django.urls import reverse
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render
# from .forms import UploadFileForm

# .models cunku ayni app in icindeki 2 dosya views.py ve models.py
# .models yazinca .py uzantisina gerek kalmiyor.

from itertools import chain


def home(request):
    if request.user.is_active:
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        lecture = lectureQueryset.filter(period=p)

        if request.user.groups.filter(name="Instructor").exists():
            instructor = Instructor.objects.get(instructor_id=request.user)
            lecture = lecture.filter(instructor=instructor)

        elif request.user.groups.filter(name="Assistant").exists():
            print("asistan ifi")
            # print(request.user.groups)
            assistant = Assistant.objects.get(assistant_id=request.user)
            lecture = assistant.given_class.all()
            # taken_class = assistant.taken_class.all()
            # announcement = Announcement.objects.filter(lecture__in=lecture).order_by('-created_date')[:5]
            # course_material = CourseMaterial.objects.filter(lecture__in=lecture).order_by('-created_date')[:5]
            # assignment = Assignment.objects.filter(lecture__in=lecture).order_by('-created_date')[:5]
            # grade = Grade.objects.filter(lecture__in=lecture).order_by('-created_date')[:3]
            # notification = list(announcement) + list(course_material) + list(assignment) + list(grade)
            # notification = sorted(notification, key=lambda x: x.created_date)
            # notification = notification.__reversed__()
            # return render(request, 'Home.html', {'notifications': notification, 'taken_classes': taken_class, 'lectures': lecture, 'AuthenticationForm': AuthenticationForm})

        elif request.user.groups.filter(name="Student").exists():
            student = Student.objects.get(student_id=request.user)
            lecture = lecture.filter(student=student)
            announcement = Announcement.objects.filter(lecture__in=lecture).order_by('-created_date')[:5]
            course_material = CourseMaterial.objects.filter(lecture__in=lecture).order_by('-created_date')[:5]
            assignment = Assignment.objects.filter(lecture__in=lecture).order_by('-created_date')[:5]
            grade = Grade.objects.filter(lecture__in=lecture).order_by('-created_date')[:3]
            notification = list(announcement) + list(course_material) + list(assignment) +list(grade)
            notification = sorted(notification, key=lambda x: x.created_date)
            notification = notification.__reversed__()
            # notification = notification.order_by('created_date')
            return render(request, 'Home.html', {'notifications': notification, 'lectures': lecture, 'AuthenticationForm': AuthenticationForm})

        return render(request, 'Home.html', {'lectures': lecture, 'AuthenticationForm': AuthenticationForm})

    else:
        return render(request, 'Home.html', {'AuthenticationForm': AuthenticationForm})


@login_required(login_url='/Home')
def announcements(request, pk):
    if request.user.is_active:
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        d = Lecture.objects.get(id=pk)
        lecture = lectureQueryset.filter(period=p)
        if request.user.groups.filter(name="Instructor").exists():
            instructor = Instructor.objects.get(instructor_id=request.user)
            lecture = lecture.filter(instructor=instructor)
        elif request.user.groups.filter(name="Assistant").exists():
            assistant = Assistant.objects.get(assistant_id=request.user)
            lecture = assistant.given_class.all()
            takenClass = assistant.taken_class.all()
        else:
            student = Student.objects.get(student_id=request.user)
            lecture = lecture.filter(student=student)
        announcement = Announcement.objects.filter(lecture__name=d)
        return render(request, 'Announcements.html', {'lectures': lecture, 'announcements': announcement, 'AuthenticationForm': AuthenticationForm})
    else:
        return render(request, 'Home.html', {'AuthenticationForm': AuthenticationForm})


# def relevantLectures(request):
#     # if request.user == "Instructor":
#     lecture = Lecture.objects.order_by('name')
#     return render(request, 'deneme.html', {'relevantLectures': lecture, 'AuthenticationForm': AuthenticationForm})

# deneme
@login_required(login_url='/Home')
def announcements_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    # return render(request, 'announcements_detail.html', {'announcements': announcement})
    # deniyorum
    if request.user.is_active:
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        # d = Lecture.objects.get(id=pk)
        lecture = lectureQueryset.filter(period=p)
        if request.user.groups.filter(name="Instructor").exists():
            instructor = Instructor.objects.get(instructor_id=request.user)
            lecture = lecture.filter(instructor=instructor)
        elif request.user.groups.filter(name="Assistant").exists():
            assistant = Assistant.objects.get(assistant_id=request.user)
            lecture = assistant.given_class.all()
        else:
            student = Student.objects.get(student_id=request.user)
            lecture = lecture.filter(student=student)
        if lecture.filter(id=announcement.lecture.id):
            return render(request, 'announcements_detail.html', {'lectures': lecture, 'announcements': announcement})
        return HttpResponseRedirect(reverse('Announcement', args=(announcement.lecture_id,)))

def isInstructor(user):
    return user.instructor


def isAssistant(user):
    return user.assistant


# @user_passes_test(isInstructor)
def add_announcement(request, path):
    index = int([i for i in str(path).split('/') if i][-2])

    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.created_date = timezone.now()
            announcement.lecture = Lecture.objects.get(id=index)
            announcement.save()
            return HttpResponseRedirect(reverse('Announcement', args=(index,)))
    else:
        form = AnnouncementForm()
    return HttpResponseRedirect(reverse('Announcement', args=(index,)))


def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.user.is_active:
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        # d = Lecture.objects.get(id=pk)
        lecture = lectureQueryset.filter(period=p)
        if request.user.groups.filter(name="Instructor").exists():
            instructor = Instructor.objects.get(instructor_id=request.user)
            lecture = lecture.filter(instructor=instructor)
        elif request.user.groups.filter(name="Assistant").exists():
            assistant = Assistant.objects.get(assistant_id=request.user)
            lecture = assistant.given_class.all()
        else:
            student = Student.objects.get(student_id=request.user)
            lecture = lecture.filter(student=student)
        # announcement id si, verdiğim derslerden birine eşit mi
        # announcement benim verdiğim bir derse mi ait
        if lecture.filter(id=announcement.lecture.id):
            if request.method == "POST":
                form = AnnouncementForm(request.POST, instance=announcement)
                if form.is_valid():
                    announcement = form.save(commit=False)
                    announcement.author = request.user
                    announcement.created_date = timezone.now()
                    announcement.save()
                    return HttpResponseRedirect(reverse('Announcement',
                                                        args=(announcement.lecture_id,)))
            else:
                form = AnnouncementForm(instance=announcement)
            return render(request, 'edit_announcement.html', {'form': form})
        return HttpResponseRedirect(reverse('Announcement',
                                            args=(announcement.lecture_id,)))

@login_required(login_url='/Login')
def delete_announcement(request):
    pk = request.POST.get("pk", None)
    obj = get_object_or_404(Announcement, pk=pk)
    id = obj.lecture_id
    obj.delete()
    return HttpResponseRedirect(reverse('Announcement', args=(id,)))


def login_request(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    userid = user
    if user is not None:
        login(request, user)
        return redirect('/', {'logged_in'})
    else:
        messages.error(request, 'username or password not correct')
        return redirect('/')


def logout_request(request):
    if request.method == "POST":
        logout(request)
    return redirect('Home')


# def deneme(request):
#     return render(request, 'deneme.html', {})


# düzenle
@login_required(login_url='/Login')
def course_materials(request, pk):
    if request.user.is_active:
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        d = Lecture.objects.get(id=pk)
        lecture = lectureQueryset.filter(period=p)
        if request.user.groups.filter(name="Instructor").exists():
            instructor = Instructor.objects.get(instructor_id=request.user)
            lecture = lecture.filter(instructor=instructor)
        elif request.user.groups.filter(name="Assistant").exists():
            assistant = Assistant.objects.get(assistant_id=request.user)
            lecture = assistant.given_class.all()
        else:
            student = Student.objects.get(student_id=request.user)
            lecture = lecture.filter(student=student)
        courseMaterial = CourseMaterial.objects.filter(lecture__name=d)
        return render(request, 'course_materials.html', {'lectures': lecture, 'courseMaterials': courseMaterial, 'AuthenticationForm': AuthenticationForm})
    else:
        return render(request, 'course_materials.html', {'AuthenticationForm': AuthenticationForm})

    # if request.user.is_active:
    #     lectureQueryset = Lecture.objects.all()
    #     p = "fall2018"
    #     d = Lecture.objects.get(id=pk)
    #     lecture = lectureQueryset.filter(period=p)
    #     if request.user.groups.filter(name="Instructor").exists():
    #         instructor = Instructor.objects.get(instructor_id=request.user)
    #         lecture = lecture.filter(instructor=instructor)
    #     elif request.user.groups.filter(name="Assistant").exists():
    #         assistant = Assistant.objects.get(assistant_id=request.user)
    #         lecture = assistant.given_class.all()
    #         takenClass = assistant.taken_class.all()
    #     else:
    #         student = Student.objects.get(student_id=request.user)
    #         lecture = lecture.filter(student=student)
    #     announcement = Announcement.objects.filter(lecture__name=d)
    #     return render(request, 'Announcements.html', {'lectures': lecture, 'announcements': announcement, 'AuthenticationForm': AuthenticationForm})
    # else:
    #     return render(request, 'Home.html', {'AuthenticationForm': AuthenticationForm})



@login_required(login_url='/Login')
def student_upload(request, path):
    index = int([i for i in str(path).split('/') if i][-1])
    if request.method == 'POST':
        form = StudentUploadFileForm(request.POST, request.FILES or None)
        print("form method post")
        if form.is_valid():
            print("form valid")
            assignment = Assignment.objects.get(id=index)
            students_upload = StudentUploadFile.objects.filter(
                author_id=request.user.id).filter(student_upload=assignment).first()
            upload = form.save(commit=False)
            # eğer emrenin assignment ı vars ave request.FILES varsa, emrenin assignmentını sil ve alt satırdakini ekle
            if Assignment.objects.get(pk=index).due_date > timezone.now():
                if students_upload is not None:
                    students_upload.delete()
                    students_upload.doc_file = request.FILES['doc_file']
                    students_upload.author = request.user
                    students_upload.created_date = timezone.now()
                    students_upload.save()
                    messages.success(request, 'Assignment successfully sent.')
                    return HttpResponseRedirect(reverse('assignments_detail', args=(index,)))

                else:
                    if request.FILES:
                        upload.doc_file = request.FILES['doc_file']
                    upload.student_upload = Assignment.objects.get(id=index)
                    upload.author = request.user
                    upload.created_date = timezone.now()
                    upload.save()
                    messages.success(request, 'Assignment successfully sent.')
                    return HttpResponseRedirect(reverse('assignments_detail', args=(index,)))

            else:
                messages.error(request, 'Due time is expired.')
        else:
            messages.error(request, 'Missing File.')

    return HttpResponseRedirect(reverse('assignments_detail', args=(index,)))


#MultiValueDictKeyError alıyor doc_file (eğer dosya eklenmezsem)
def upload_course_material(request, path):
    index = int([i for i in str(path).split('/') if i][-2])
    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES or None)
        if form.is_valid():
            course_material = form.save(commit=False)
            if request.FILES:
                course_material.doc_file = request.FILES['doc_file']
            course_material.lecture = Lecture.objects.get(id=index)
            course_material.author = request.user
            course_material.created_date = timezone.now()
            course_material.save()

            return HttpResponseRedirect(reverse('course_materials', args=(index,)))
    else:
        form = CourseMaterialForm()

    return HttpResponseRedirect(reverse('course_materials', args=(index,)))


@login_required(login_url='/Home')
def course_materials_detail(request, pk):
    course_material = get_object_or_404(CourseMaterial, pk=pk)
    # return render(request, 'course_materials_detail.html', {'course_materials': course_material})
    if request.user.is_active:
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        # d = Lecture.objects.get(id=pk)
        lecture = lectureQueryset.filter(period=p)
        if request.user.groups.filter(name="Instructor").exists():
            instructor = Instructor.objects.get(instructor_id=request.user)
            lecture = lecture.filter(instructor=instructor)
        elif request.user.groups.filter(name="Assistant").exists():
            assistant = Assistant.objects.get(assistant_id=request.user)
            lecture = assistant.given_class.all()
        else:
            student = Student.objects.get(student_id=request.user)
            lecture = lecture.filter(student=student)
        if lecture.filter(id=course_material.lecture.id):
            return render(request, 'course_materials_detail.html', {'lectures': lecture, 'course_materials': course_material})
        return HttpResponseRedirect(reverse('course_materials', args=(course_material.lecture_id,)))


    # if lecture.filter(id=announcement.lecture.id):
    #     return render(request, 'announcements_detail.html', {'lectures': lecture, 'announcements': announcement})
    # return HttpResponseRedirect(reverse('Announcement', args=(announcement.lecture_id,)))


#MultiValueDictKeyError alıyor doc_file
@login_required(login_url='/Login')
def edit_course_material(request, pk):
    course_material = get_object_or_404(CourseMaterial, pk=pk)
    if request.user.is_active:
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        # d = Lecture.objects.get(id=pk)
        lecture = lectureQueryset.filter(period=p)
        if request.user.groups.filter(name="Instructor").exists():
            instructor = Instructor.objects.get(instructor_id=request.user)
            lecture = lecture.filter(instructor=instructor)
        elif request.user.groups.filter(name="Assistant").exists():
            assistant = Assistant.objects.get(assistant_id=request.user)
            lecture = assistant.given_class.all()
        else:
            student = Student.objects.get(student_id=request.user)
            lecture = lecture.filter(student=student)
        if lecture.filter(id=course_material.lecture.id):
            if request.method == "POST":
                form = CourseMaterialForm(request.POST, request.FILES, instance=course_material)
                if form.is_valid():
                    course_material = form.save(commit=False)
                    id = course_material.lecture_id
                    if request.FILES:
                        course_material.doc_file = request.FILES['doc_file']
                    course_material.author = request.user
                    course_material.created_date = timezone.now()
                    course_material.save()
                    return HttpResponseRedirect(reverse('course_materials', args=(id,)))
            else:
                form = CourseMaterialForm(instance=course_material)
            return render(request, 'edit_course_materials.html', {'form': form})
        return HttpResponseRedirect(reverse('course_materials', args=(course_material.lecture_id,)))


@login_required(login_url='/Login')
def delete_course_material(request):
    pk = request.POST.get("pk", None)
    obj = get_object_or_404(CourseMaterial, pk=pk)
    id = obj.lecture_id
    obj.delete()
    return HttpResponseRedirect(reverse('course_materials', args=(id,)))


@login_required(login_url='/Home')
def lecture(request, pk):
    lecture_content = get_object_or_404(Lecture, pk=pk)
    # return render(request, "lectureContent.html", {'lecture_content': lecture_content})
    if request.user.is_active:
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        d = Lecture.objects.get(id=pk)
        lecture = lectureQueryset.filter(period=p)
        if request.user.groups.filter(name="Instructor").exists():
            instructor = Instructor.objects.get(instructor_id=request.user)
            lecture = lecture.filter(instructor=instructor)
        elif request.user.groups.filter(name="Assistant").exists():
            assistant = Assistant.objects.get(assistant_id=request.user)
            lecture = assistant.given_class.all()
        else:
            student = Student.objects.get(student_id=request.user)
            lecture = lecture.filter(student=student)
        return render(request, 'lectureContent.html', {'lectures': lecture, 'lecture_content': lecture_content, 'AuthenticationForm': AuthenticationForm})
    else:
        return render(request, 'Home.html', {'AuthenticationForm': AuthenticationForm})


@login_required(login_url='/Home')
def assignments(request, pk):
    if request.user.is_active:
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        d = Lecture.objects.get(id=pk)
        lecture = lectureQueryset.filter(period=p)
        if request.user.groups.filter(name="Instructor").exists():
            instructor = Instructor.objects.get(instructor_id=request.user)
            lecture = lecture.filter(instructor=instructor)
        elif request.user.groups.filter(name="Assistant").exists():
            assistant = Assistant.objects.get(assistant_id=request.user)
            lecture = assistant.given_class.all()
        else:
            student = Student.objects.get(student_id=request.user)
            lecture = lecture.filter(student=student)
        assignment = Assignment.objects.filter(lecture__name=d)
        return render(request, 'assignments.html', {'lectures': lecture, 'assignments': assignment, 'AuthenticationForm': AuthenticationForm})
    else:
        return render(request, 'assignments.html', {'AuthenticationForm': AuthenticationForm})


@login_required(login_url='/Home')
def assignments_detail(request, pk):
    if request.user.is_active:
        assignment = get_object_or_404(Assignment, pk=pk)
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        lecture = lectureQueryset.filter(period=p)
        if request.user.is_active:
            lectureQueryset = Lecture.objects.all()
            p = "fall2018"
            # d = Lecture.objects.get(id=pk)
            lecture = lectureQueryset.filter(period=p)
            if request.user.groups.filter(name="Instructor").exists():
                instructor = Instructor.objects.get(instructor_id=request.user)
                lecture = lecture.filter(instructor=instructor)
            elif request.user.groups.filter(name="Assistant").exists():
                assistant = Assistant.objects.get(assistant_id=request.user)
                lecture = assistant.given_class.all()
            else:
                student = Student.objects.get(student_id=request.user)
                lecture = lecture.filter(student=student)
            if lecture.filter(id=assignment.lecture.id):
                if request.user.groups.filter(name="Instructor").exists():
                    instructor = Instructor.objects.get(instructor_id=request.user)
                    lecture = lecture.filter(instructor=instructor)
                    uploadQueryset = StudentUploadFile.objects.all()
                    uploadSet = uploadQueryset.filter(student_upload=assignment)
                    return render(request, 'assignments_detail.html', {'assignments': assignment,
                                                                       'upload_sets': uploadSet,
                                                                       'lectures': lecture})
                elif request.user.groups.filter(name="Assistant").exists():
                    uploadQueryset = StudentUploadFile.objects.all()
                    uploadSet = uploadQueryset.filter(student_upload=assignment)
                    return render(request, 'assignments_detail.html', {'assignments': assignment,
                                                                       'upload_sets': uploadSet,
                                                                       'lectures': lecture})
                elif request.user.groups.filter(name="Student").exists():
                    uploadQueryset = StudentUploadFile.objects.all()
                    uploadSet = uploadQueryset.filter(student_upload=assignment)
                    uploadSet_student = uploadSet.filter(author_id=request.user)
                    return render(request, 'assignments_detail.html', {'assignments': assignment,
                                                                       'upload_sets': uploadSet_student,
                                                                       'lectures': lecture})
            return HttpResponseRedirect(reverse('assignments', args=(assignment.lecture_id,)))


#MultiValueDictKeyError alıyor doc_file (eğer dosya eklenmezsem)
#due_date eklemezsem de hata alıyorum
def upload_assignment(request, path):
    index = int([i for i in str(path).split('/') if i][-2])
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES or None)
        if form.is_valid():
            assignment = form.save(commit=False)
            if request.FILES:
                assignment.doc_file = request.FILES['doc_file']

            assignment.lecture = Lecture.objects.get(id=index)
            assignment.author = request.user
            assignment.created_date = timezone.now()
            assignment.save()

            return HttpResponseRedirect(reverse('assignments', args=(index,)))
    else:
        form = AssignmentForm()

    return HttpResponseRedirect(reverse('assignments', args=(index,)))


#MultiValueDictKeyError alıyor doc_file
def edit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.user.is_active:
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        # d = Lecture.objects.get(id=pk)
        lecture = lectureQueryset.filter(period=p)
        if request.user.groups.filter(name="Instructor").exists():
            instructor = Instructor.objects.get(instructor_id=request.user)
            lecture = lecture.filter(instructor=instructor)
        elif request.user.groups.filter(name="Assistant").exists():
            assistant = Assistant.objects.get(assistant_id=request.user)
            lecture = assistant.given_class.all()
        else:
            student = Student.objects.get(student_id=request.user)
            lecture = lecture.filter(student=student)
        if lecture.filter(id=assignment.lecture.id):
            if request.method == "POST":
                form = AssignmentForm(request.POST, request.FILES, instance=assignment)
                if form.is_valid():

                    assignment = form.save(commit=False)
                    if request.FILES:
                        assignment.doc_file = request.FILES['doc_file']
                    # assignment.lecture = Lecture.objects.get(id=index)
                    assignment.author = request.user
                    assignment.created_date = timezone.now()
                    assignment.save()
                    return HttpResponseRedirect(reverse('assignments',
                                                        args=(assignment.lecture_id,)))
            else:
                form = AssignmentForm(instance=assignment)
            return render(request, 'edit_assignment.html', {'form': form})
        return HttpResponseRedirect(reverse('assignments', args=(assignment.lecture_id,)))



@login_required(login_url='/Login')
def delete_assignment(request):
    pk = request.POST.get("pk", None)
    obj = get_object_or_404(Assignment, pk=pk)
    id = obj.lecture_id
    obj.delete()
    return HttpResponseRedirect(reverse('assignments', args=(id,)))


@login_required(login_url='/Home')
def grades(request, pk):
    if request.user.is_active:
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        d = Lecture.objects.get(id=pk)
        lecture = lectureQueryset.filter(period=p)
        if request.user.groups.filter(name="Instructor").exists():
            instructor = Instructor.objects.get(instructor_id=request.user)
            lecture = lecture.filter(instructor=instructor)
        elif request.user.groups.filter(name="Assistant").exists():
            assistant = Assistant.objects.get(assistant_id=request.user)
            lecture = assistant.given_class.all()
        else:
            student = Student.objects.get(student_id=request.user)
            lecture = lecture.filter(student=student)
        grade = Grade.objects.filter(lecture__name=d)
        return render(request, 'grades.html', {'lectures': lecture, 'grades': grade, 'AuthenticationForm': AuthenticationForm})
    else:
        return render(request, 'home.html', {'AuthenticationForm': AuthenticationForm})



@login_required(login_url='/Home')
def grades_detail(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    # return render(request, 'grades_detail.html', {'grades': grade})
    if request.user.is_active:
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        # d = Lecture.objects.get(id=pk)
        lecture = lectureQueryset.filter(period=p)
        if request.user.groups.filter(name="Instructor").exists():
            instructor = Instructor.objects.get(instructor_id=request.user)
            lecture = lecture.filter(instructor=instructor)
        elif request.user.groups.filter(name="Assistant").exists():
            assistant = Assistant.objects.get(assistant_id=request.user)
            lecture = assistant.given_class.all()
        else:
            student = Student.objects.get(student_id=request.user)
            lecture = lecture.filter(student=student)
        # grade = Grade.objects.filter(lecture__name=d)
        return render(request, 'grades_detail.html', {'lectures': lecture, 'grades': grade, 'AuthenticationForm': AuthenticationForm})
    else:
        return render(request, 'home.html', {'AuthenticationForm': AuthenticationForm})


#MultiValueDictKeyError alıyor doc_file (eğer dosya eklenmezsem)
def upload_grade(request, path):
    index = int([i for i in str(path).split('/') if i][-2])
    if request.method == 'POST':
        form = GradeForm(request.POST, request.FILES or None)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.doc_file = request.FILES['doc_file']
            grade.lecture = Lecture.objects.get(id=index)
            grade.author = request.user
            grade.created_date = timezone.now()
            grade.save()

            return HttpResponseRedirect(reverse('grades', args=(index,)))
    else:
        form = GradeForm()

    return HttpResponseRedirect(reverse('grades', args=(index,)))


#MultiValueDictKeyError alıyor doc_file
@login_required(login_url='/Login')
def edit_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.user.is_active:
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        # d = Lecture.objects.get(id=pk)
        lecture = lectureQueryset.filter(period=p)
        if request.user.groups.filter(name="Instructor").exists():
            instructor = Instructor.objects.get(instructor_id=request.user)
            lecture = lecture.filter(instructor=instructor)
        elif request.user.groups.filter(name="Assistant").exists():
            assistant = Assistant.objects.get(assistant_id=request.user)
            lecture = assistant.given_class.all()
        else:
            student = Student.objects.get(student_id=request.user)
            lecture = lecture.filter(student=student)
        if lecture.filter(id=grade.lecture.id):
            if request.method == "POST":
                form = GradeForm(request.POST, request.FILES, instance=grade)
                if form.is_valid():
                    grade = form.save(commit=False)
                    id = grade.lecture_id
                    if request.FILES:
                        grade.doc_file = request.FILES['doc_file']
                    grade.author = request.user
                    grade.created_date = timezone.now()
                    grade.save()
                    return HttpResponseRedirect(reverse('grades', args=(id,)))

            else:
                form = GradeForm(instance=grade)
            return render(request, 'edit_grade.html', {'form': form})
        return HttpResponseRedirect(reverse('grades', args=(grade.lecture_id,)))


@login_required(login_url='/Login')
def delete_grade(request):
    pk = request.POST.get("pk", None)
    obj = get_object_or_404(Grade, pk=pk)
    id = obj.lecture_id
    obj.delete()
    return HttpResponseRedirect(reverse('grades', args=(id,)))


@login_required(login_url='/Home')
def search(request):
    if request.user.is_active and request.method == "POST" or request.method == "GET":
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        # d = Lecture.objects.get(id=pk)
        lecture = lectureQueryset.filter(period=p)
        if request.user.groups.filter(name="Instructor").exists():
            instructor = Instructor.objects.get(instructor_id=request.user)
            lecture = lecture.filter(instructor=instructor)
        elif request.user.groups.filter(name="Assistant").exists():
            assistant = Assistant.objects.get(assistant_id=request.user)
            lecture = assistant.given_class.all()
        else:
            student = Student.objects.get(student_id=request.user)
            lecture = lecture.filter(student=student)

        lectureQueryset = ""
        if request.method == "POST":
            if request.POST['word'] is not None:
                word = request.POST['word']
                lectureQueryset = Lecture.objects.all()
                lectureQueryset = lectureQueryset.filter(name__icontains=word)
        return render(request, 'search.html', {'lectureQueryset': lectureQueryset, 'lectures': lecture})

    else:
        return render(request, 'search.html', {'AuthenticationForm': AuthenticationForm})


@login_required(login_url='/Home')
def syllabus(request, pk):
    if request.user.is_active:
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        d = Lecture.objects.get(id=pk)
        lecture = lectureQueryset.filter(period=p)
        if request.user.groups.filter(name="Instructor").exists():
            instructor = Instructor.objects.get(instructor_id=request.user)
            lecture = lecture.filter(instructor=instructor)
        elif request.user.groups.filter(name="Assistant").exists():
            assistant = Assistant.objects.get(assistant_id=request.user)
            lecture = assistant.given_class.all()
        else:
            student = Student.objects.get(student_id=request.user)
            lecture = lecture.filter(student=student)
        syllabus = Syllabus.objects.filter(lecture__name=d)
        return render(request, 'syllabus.html',
                      {'lectures': lecture, 'syllabus': syllabus, 'AuthenticationForm': AuthenticationForm})
    else:
        return render(request, 'Home.html', {'AuthenticationForm': AuthenticationForm})


@login_required(login_url='/Login')
def add_syllabus(request, path):
    index = int([i for i in str(path).split('/') if i][-2])
    if request.method == 'POST':
        form = SyllabusForm(request.POST, request.FILES or None)
        print("form method post")
        if form.is_valid():
            print("form valid")
            lecture = Lecture.objects.get(id=index)
            syllabus = Syllabus.objects.filter(
                author_id=request.user.id).filter(lecture=lecture).first()
            upload = form.save(commit=False)
            # eğer syllabus varsa ve request.FILES varsa, mevcut syllabus ı sil ve alt satırdakini ekle
            # if Assignment.objects.get(pk=index).due_date > timezone.now():
            if syllabus is not None:
                syllabus.delete()
                syllabus.doc_file = request.FILES['doc_file']
                syllabus.author = request.user
                syllabus.created_date = timezone.now()
                syllabus.save()
                messages.success(request, 'Syllabus successfully sent.')
                return HttpResponseRedirect(reverse('syllabus', args=(index,)))
            else:
                if request.FILES:
                    upload.doc_file = request.FILES['doc_file']
                upload.lecture = Lecture.objects.get(id=index)
                upload.author = request.user
                upload.created_date = timezone.now()
                upload.save()
                messages.success(request, 'Assignment successfully sent.')
                return HttpResponseRedirect(reverse('syllabus', args=(index,)))

            # else:
            #     messages.error(request, 'Due time is expired.')
        else:
            messages.error(request, 'Missing File.')

    return HttpResponseRedirect(reverse('syllabus', args=(index,)))


@login_required(login_url='/Login')
def delete_syllabus(request):
    pk = request.POST.get("pk", None)
    obj = get_object_or_404(Syllabus, pk=pk)
    id = obj.lecture_id
    obj.delete()
    return HttpResponseRedirect(reverse('syllabus', args=(id,)))


def assistants(request, pk):
    if request.user.is_active:
        print(pk)
        lectureQueryset = Lecture.objects.all()
        p = "fall2018"
        d = Lecture.objects.get(id=pk)
        lecture = lectureQueryset.filter(period=p)
        assistantQueryset = Assistant.objects.all()

        if request.user.groups.filter(name="Instructor").exists():
            instructor = Instructor.objects.get(instructor_id=request.user)
            lecture = lecture.filter(instructor=instructor)
            # assistant = get_object_or_404(Assistant)
            assistant = assistantQueryset.filter(given_class__in=lecture)
            # announcement = Announcement.objects.filter(lecture__name=d)
            # givenClass = assistant.given_class.all()

            if Assistant.objects.filter(given_class=d):
                assistant = assistantQueryset.filter(given_class=Lecture.objects.get(id=pk))
                return render(request, 'assistants.html',
                      {'lectures': lecture, 'assistants': assistant,'AuthenticationForm': AuthenticationForm})
            else:
                assistant = Assistant.objects.none()
                return render(request, 'assistants.html',
                              {'lectures': lecture, 'assistants': assistant, 'AuthenticationForm': AuthenticationForm})
        return HttpResponseRedirect(reverse('lecture'))
    else:
        return render(request, 'Home.html', {'AuthenticationForm': AuthenticationForm})


@user_passes_test(isInstructor)
def add_assistant(request, path):
    index = int([i for i in str(path).split('/') if i][-2])
    print("geldi, lecture id", index)
    if request.user.is_active and request.method == "POST" or request.method == "GET":
        print("ekleyeceğim lecture:", Lecture.objects.get(id=index))
        lecture = Lecture.objects.get(id=index)
        if request.method == "POST":
            if request.POST['word'] is not None:
                print("girdi:",request.POST['word'])
                word = request.POST['word']
                if Assistant.objects.filter(assistant_id__username=word).exists():
                    print("var")
                    assistant = Assistant.objects.get(assistant_id__username=request.POST['word'])
                # assistant = Assistant.objects.get(assistant_name="Tuğba Erkoç")
                # assistant = assistantQueryset.filter(Assistant.assistant_id = "assistant@isik.edu.tr")
                    print("eşleşen asistan:", assistant)
                    print("verdiği dersler", assistant.given_class.all())
                    assistant.given_class.add(lecture)
                    assistant.save()
                    return HttpResponseRedirect(reverse('assistants', args=(index,)))
    return HttpResponseRedirect(reverse('assistants', args=(index,)))


@user_passes_test(isInstructor)
def delete_assistant(request, path):
    index = int([i for i in str(path).split('/') if i][-2])
    print("geldi, lecture id", index)
    if request.user.is_active and request.method == "POST" or request.method == "GET":
        print("sileceğim lecture:", Lecture.objects.get(id=index))
        lecture = Lecture.objects.get(id=index)
        if request.method == "POST":
            if request.POST['word'] is not None:
                word = request.POST['word']
                assistant = Assistant.objects.get(pk=word)
                assistant.given_class.remove(lecture)
                assistant.save()
                return HttpResponseRedirect(reverse('assistants', args=(index,)))

    return HttpResponseRedirect(reverse('assistants', args=(index,)))



    # if request.user.is_active and request.method == "POST" or request.method == "GET":
    #     lectureQueryset = Lecture.objects.all()
    #     p = "fall2018"
    #     # d = Lecture.objects.get(id=pk)
    #     lecture = lectureQueryset.filter(period=p)
    #     if request.user.groups.filter(name="Instructor").exists():
    #         instructor = Instructor.objects.get(instructor_id=request.user)
    #         lecture = lecture.filter(instructor=instructor)
    #     elif request.user.groups.filter(name="Assistant").exists():
    #         assistant = Assistant.objects.get(assistant_id=request.user)
    #         lecture = assistant.given_class.all()
    #     else:
    #         student = Student.objects.get(student_id=request.user)
    #         lecture = lecture.filter(student=student)
    #
    #     lectureQueryset = ""
    #     if request.method == "POST":
    #         if request.POST['word'] is not None:
    #             word = request.POST['word']
    #             lectureQueryset = Lecture.objects.all()
    #             lectureQueryset = lectureQueryset.filter(name__icontains=word)
    #     return render(request, 'search.html', {'lectureQueryset': lectureQueryset, 'lectures': lecture})
    #
    # else:
    #     return render(request, 'search.html', {'AuthenticationForm': AuthenticationForm})


# #düzenlenecek, denenmedi
# def edit_assistant(request, pk):
#     assistant = get_object_or_404(Assistant, pk=pk)
#     if request.method == "POST":
#         form = AssistantForm(request.POST, instance=assistant)
#         if form.is_valid():
#             assistant = form.save(commit=False)
#             givenClass = assistant.given_class
#             assistant.save()
#             return HttpResponseRedirect(reverse('assistants',
#                                                 args=(givenClass,)))

    # else:
    #     form = AssistantForm(instance=assistant)
    # return render(request, 'edit_assistants.html', {'form': form})
    #
#
# #düzenlenecek, denenmedi
# @login_required(login_url='/Login')
# def delete_assistant(request):
#     # pk = request.POST.get("pk", None)
#     obj = get_object_or_404(Assistant)
#     id = obj.given_class
#     obj.delete()
#     return HttpResponseRedirect(reverse('assistants', args=(id,)))
