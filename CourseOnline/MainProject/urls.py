from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls. static import static

urlpatterns = [
    #'html adresi' - viewstaki method adı - sıradan isim
    path('', views.home, name='Home'),
    path('login/', views.login_request, name='Login'),
    path('logout/', views.logout_request, name="Logout"),
    path('lecture/<int:pk>/', views.lecture, name='lecture'),
    path('search', views.search, name='search'),
    path('student_upload/<path:path>', views.student_upload, name='student_upload'),

    path('lecture/<int:pk>/assistants/', views.assistants, name='assistants'),
    path('add_assistant/<path:path>', views.add_assistant, name='add_assistant'),
    path('delete_assistant/<path:path>', views.delete_assistant, name='delete_assistant'),

    path('lecture/<int:pk>/syllabus/', views.syllabus, name='syllabus'),
    path('add_syllabus/<path:path>', views.add_syllabus, name='add_syllabus'),
    path('delete_syllabus', views.delete_syllabus, name='delete_syllabus'),

    path('lecture/<int:pk>/Announcements/', views.announcements, name='Announcement'),
    path('Announcements/<int:pk>/', views.announcements_detail, name='announcements_detail'),
    path('add_announcement/<path:path>', views.add_announcement, name='add_announcement'),
    path('Announcements/<int:pk>/edit_announcement/', views.edit_announcement, name='edit_announcement'),
    path('delete_announcement', views.delete_announcement, name='delete_announcement'),

    path('lecture/<int:pk>/course_materials', views.course_materials, name='course_materials'),
    path('upload_course_material/<path:path>', views.upload_course_material, name='upload_course_material'),
    path('course_materials/<int:pk>/', views.course_materials_detail, name='course_materials_detail'),
    path('course_materials/<int:pk>/edit_course_material/', views.edit_course_material, name='edit_course_material'),
    path('delete_course_material', views.delete_course_material, name='delete_course_material'),

    path('lecture/<int:pk>/assignments/', views.assignments, name='assignments'),
    path('upload_assignment/<path:path>', views.upload_assignment, name='upload_assignment'),
    path('assignments/<int:pk>/', views.assignments_detail, name='assignments_detail'),
    path('assignments/<int:pk>/edit_assignment/', views.edit_assignment, name='edit_assignment'),
    path('delete_assignment', views.delete_assignment, name='delete_assignment'),

    path('lecture/<int:pk>/grades', views.grades, name='grades'),
    path('upload_grade/<path:path>', views.upload_grade, name='upload_grade'),
    path('grades/<int:pk>/', views.grades_detail, name='grades_detail'),
    path('grades/<int:pk>/edit_grade/', views.edit_grade, name='edit_grade'),
    path('delete_grade', views.delete_grade, name='delete_grade'),

    # path('list', views.list, name='list')

    # path('edit_announcement/', views.edit_announcement, name='edit_announcement'),
    # path('delete_announcement/', views.delete_announcement, name='delete_announcement')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)