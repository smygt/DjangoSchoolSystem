from django.contrib import admin
from .models import Announcement, Lecture
from .models import Instructor, Student, Assistant, Syllabus
from .models import CourseMaterial, Assignment, Grade, StudentUploadFile

# Register your models here.

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ["name", "period"]

    class Meta:
        model = Lecture


class StudentAdmin(admin.ModelAdmin):
    list_display = ["student_name", "get_classes"]
    list_display_links = ["student_name", "get_classes"]



@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ["instructor_name", "get_classes"]
    list_display_links = ["instructor_name", "get_classes"]


    class Meta:
        model = Instructor


class AssistantAdmin(admin.ModelAdmin):
    list_display = ["assistant_name", "get_classes"]
    list_display_links = ["assistant_name", "get_classes"]

    class Meta:
        model = Assistant


# admin announcement ekranını özelleştirmek için announcementları decorator
# olarak yazmak icin admin.register kullandık
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):

    # announcement ekranında hangi bilgiler gözüksün
    list_display = ["title", "lecture", "created_date", "author"]

    # announcement ekranında hangi bilgilere tıklanılabilsin
    list_display_links = ["title", "lecture", "created_date"]

    # hangi özellikler aranabilsin
    # her search_field içine tek attr alıyor.
    search_fields = ["title"]
    search_fields = ["content"]

    # hangi özelliğe göre filtreleme yapabileyim
    list_filter = ["created_date", "lecture"]

    class Meta:
        model = Announcement


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):

    # course material ekranında hangi bilgiler gözüksün
    list_display = ["title", "lecture", "created_date", "author"]

    # course material ekranında hangi bilgilere tıklanılabilsin
    list_display_links = ["title", "lecture", "created_date"]

    # hangi özellikler aranabilsin
    # her search_field içine tek attr alıyor.
    search_fields = ["title"]
    search_fields = ["doc_file"]

    # hangi özelliğe göre filtreleme yapabileyim
    list_filter = ["created_date", "lecture"]

    class Meta:
        model = CourseMaterial



@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):

    # Assignment ekranında hangi bilgiler gözüksün
    list_display = ["title", "lecture", "created_date", "author", "due_date"]

    # Assignment ekranında hangi bilgilere tıklanılabilsin
    list_display_links = ["title", "lecture", "created_date"]

    # hangi özellikler aranabilsin
    # her search_field içine tek attr alıyor.
    search_fields = ["title"]
    search_fields = ["doc_file"]

    # hangi özelliğe göre filtreleme yapabileyim
    list_filter = ["created_date", "lecture"]

    class Meta:
        model = Assignment


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):

    # course material ekranında hangi bilgiler gözüksün
    list_display = ["title", "lecture", "created_date", "author"]

    # course material ekranında hangi bilgilere tıklanılabilsin
    list_display_links = ["title", "lecture", "created_date"]

    # hangi özellikler aranabilsin
    # her search_field içine tek attr alıyor.
    search_fields = ["title"]
    search_fields = ["doc_file"]

    # hangi özelliğe göre filtreleme yapabileyim
    list_filter = ["created_date", "lecture"]

    class Meta:
        model = Grade\



@admin.register(StudentUploadFile)
class StudentUploadFileAdmin(admin.ModelAdmin):

    # course material ekranında hangi bilgiler gözüksün
    list_display = ["doc_file", "student_upload", "created_date", "author"]

    # course material ekranında hangi bilgilere tıklanılabilsin
    list_display_links = ["doc_file", "student_upload", "created_date", "author"]

    # hangi özellikler aranabilsin
    # her search_field içine tek attr alıyor.
    search_fields = ["student_upload"]
    search_fields = ["doc_file"]

    # hangi özelliğe göre filtreleme yapabileyim
    list_filter = ["created_date", "student_upload", "doc_file"]

    class Meta:
        model = StudentUploadFile


@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):

    # course material ekranında hangi bilgiler gözüksün
    list_display = ["doc_file", "lecture", "created_date", "author"]

    # course material ekranında hangi bilgilere tıklanılabilsin
    list_display_links = ["doc_file", "lecture", "created_date", "author"]

    # hangi özellikler aranabilsin
    # her search_field içine tek attr alıyor.
    search_fields = ["lecture"]
    search_fields = ["doc_file"]

    # hangi özelliğe göre filtreleme yapabileyim
    list_filter = ["created_date", "lecture", "doc_file"]

    class Meta:
        model = Syllabus


# admin.site.register(Announcement)
# admin.site.register(Lecture, LectureAdmin)
# admin.site.register(Role)
admin.site.register(Student, StudentAdmin)
# admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Assistant, AssistantAdmin)
# admin.site.register(CourseMaterial)
# admin.site.register(StudentUploadFile)
