from . import views
from .views import TestDetailView, TestResultSubmitView, ExportProgressReportView
from django.urls import path
from .views import student_progress
from .views import TeacherStudentsView, StudentProgressDetailView


app_name = 'school'

urlpatterns = [
    # URL для страницы с уроками сольфеджио
    path('solfeggio/', views.SolfeggioLessonsView.as_view(), name='solfeggio_lessons'),
    path('solfeggio/lesson/<int:pk>/', views.LessonSolfDetailView.as_view(), name='lesson_detail_solf'),
    path('test/<int:pk>/', TestDetailView.as_view(), name='test_detail'),
    path('test/<int:pk>/submit/', TestResultSubmitView.as_view(), name='test_result_submit'),
    path('progress/', student_progress, name='student_progress'),
    path('teacher/students/', TeacherStudentsView.as_view(), name='teacher_students'),
    path('teacher/student/<int:pk>/progress/', StudentProgressDetailView.as_view(), name='student_progress_detail'),
    path("tests/", views.test_list, name="test_list"),
    path('literature-lessons/', views.LiteratureLessonsView.as_view(), name='literature_lessons'),
    path('literature-lessons/lesson/<int:pk>/', views.LessonLiteratureDetailView.as_view(), name='lesson_detail_lit'),
    path('export-progress/', ExportProgressReportView.as_view(), name='export_progress_report'),

    path('ear_training_tests/', views.ear_training_tests, name='ear_training_tests'),
    path('ear_training_test/<int:test_id>/', views.ear_training_test_detail, name='ear_training_test_detail'),
    path('ear_training_test/<int:test_id>/task/<int:task_id>/', views.ear_training_task, name='ear_training_task'),
    path('submit_attempt/', views.submit_attempt, name='submit_attempt'),
    path('ear_training_test/<int:test_id>/result/', views.ear_training_test_result, name='ear_training_test_result'),
    path('ear_training_results/<str:section_name>/', views.ear_training_results_section,name='ear_training_results_section'),

]
