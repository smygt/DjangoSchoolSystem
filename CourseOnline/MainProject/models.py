from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone


# ______________________________________________________________________________________

class Lecture(models.Model):
    name = models.CharField(max_length=10)
    # syllabus = models.CharField(max_length=1000)
    period = models.CharField(max_length=10)

    #name ve period kısımları birlikte uniquetir
    class Meta:
        unique_together = ('name', 'period',)

    def saveLecture(self):
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lecture'
        verbose_name_plural = 'Lectures'
# ______________________________________________________________________________________

#
#
# class Lecturer(models.Model):
#     lecturer_id = models.OneToOneField(User, on_delete=models.CASCADE)
#     given_class = models.ManyToManyField(Lecture)
#     # given_class = models.ManyToManyField(Lecture, related_name="given_class")
#
#     def __str__(self):
#         return self.lecturer_id

# ______________________________________________________________________________________


class Student(models.Model):
    student_id = models.OneToOneField(User, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=25, null=True)
    taken_class = models.ManyToManyField(Lecture)

    def __str__(self):
        return self.student_name

    # admin panel için
    def get_classes(self):
        return "\n".join([p.name for p in self.taken_class.all()])

# _______________________________________________________________________________________


class Instructor(models.Model):
    instructor_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name="instructor")
    instructor_name = models.CharField(max_length=25, null=True)
    given_class = models.ManyToManyField(Lecture)

    def __str__(self):
        return self.instructor_name

    # admin panel için
    def get_classes(self):
        return "\n".join([p.name for p in self.given_class.all()])
# ______________________________________________________________________________________


class Assistant(models.Model):
    assistant_id = models.OneToOneField(User, on_delete=models.CASCADE)
    assistant_name = models.CharField(max_length=25, null=True)
    taken_class = models.ManyToManyField(Lecture, related_name="taken_class", blank=True)
    given_class = models.ManyToManyField(Lecture, related_name="given_class", blank=True)

    def __str__(self):
        return self.assistant_name

    # admin panel için
    def get_classes(self):
        return "\n".join([p.name for p in self.given_class.all()])
# ______________________________________________________________________________________


#deniyorum
class Announcement(models.Model):
    title = models.CharField(max_length=1000, null=True)
    content = models.CharField(max_length=1000, null=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="author")

    def saveAnnouncement(self):
        self.author = self.request.user
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        x = str(self.title)
        y = str(self.content)
        xy = (x + '\n' + y)
        return xy

    def get_announcement(self):
        return reverse("announcement", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

#  ______________________________________________________________________________________


# class Role(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # isInstructor = models.BooleanField('Instructor', default=False)
#     # isStudent = models.BooleanField('Student', default=False)
#     # isAssistant = models.BooleanField('Assistant', default=False)
#
#     instructor = Instructor
#     student = Student
#     assistant = Assistant
#
#     def saveRole(self):
#         self.save()

#  ______________________________________________________________________________________
'''
class Role(models.Model):
  ''' '''
  The Role entries are managed by the system,
  automatically created via a Django data migration.
  ''' '''
  STUDENT = 1
  TEACHER = 2
  ASSISTANT = 3

  ROLE_CHOICES = (
      (STUDENT, 'student'),
      (TEACHER, 'teacher'),
      (ASSISTANT, 'assistant'),
  )

  id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

  def __str__(self):
      return self.get_id_display()


class User(AbstractUser):
  roles = models.ManyToManyField(Role)
'''
#  ______________________________________________________________________________________


class Assignment(models.Model):
    title = models.CharField(max_length=1000, null=True)
    # null=True : Django stores empty values as NULL in the database. Its default is False.
    content = models.CharField(max_length=1000, null=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)
    # blank=True : The field is allowed to be blank. Default is False.
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    due_date = models.DateTimeField(default=timezone.now, null=True)
    # due_date = models.DateField()
    # auto_now = Useful for "last-modified" timestamps
    # auto_now_add = Useful for creation of timestamps.
    # useful link : https://github.com/MongoEngine/mongoengine/issues/21
    doc_file = models.FileField(null=True)

    class Meta:
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'


class CourseMaterial(models.Model):
    title = models.CharField(max_length=1000, null=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    doc_file = models.FileField(null=True, blank=True)

    class Meta:
        verbose_name = 'CourseMaterial'
        verbose_name_plural = 'CourseMaterials'


class Grade(models.Model):
    title = models.CharField(max_length=1000, null=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    doc_file = models.FileField(null=True)


class StudentUploadFile(models.Model):
    doc_file = models.FileField(null=True)
    student_upload = models.ForeignKey(Assignment, on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Syllabus(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True, related_name="syllabus")
    doc_file = models.FileField(null=True)
