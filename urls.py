from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # Submit route
    path('course/<int:course_id>/submit/', views.submit, name='submit'),
    # Exam result route WITH required 'course/' prefix
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
]
