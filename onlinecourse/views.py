from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.order_by('-pub_date')[:10]


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'


def enroll(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        user = request.user
        if not user.is_authenticated:
            return redirect('onlinecourse:login')
        Enrollment.objects.get_or_create(user=user, course=course)
        return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    
    if not user.is_authenticated:
        return redirect('onlinecourse:login')
        
    enrollment = Enrollment.objects.get(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    
    selected_ids = request.POST.getlist('choice')
    if not selected_ids:
        selected_ids = [value for key, value in request.POST.items() if key.startswith('choice_')]
        
    for choice_id in selected_ids:
        choice = get_object_or_404(Choice, pk=int(choice_id))
        submission.choices.add(choice)
        
    submission.save()
    return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_choices = submission.choices.all()
    selected_ids = [choice.id for choice in selected_choices]
    
    total_score = 0
    total_grade = 0
    
    questions = course.question_set.all()
    for question in questions:
        total_grade += question.grade
        if question.is_get_score(selected_ids):
            total_score += question.grade
            
    grade_percentage = int((total_score / total_grade) * 100) if total_grade > 0 else 0
    
    # FIXED: Context includes all expected keys ('grade', 'total_score', 'total_grade', 'possible_score')
    context = {
        'course': course,
        'submission': submission,
        'selected_ids': selected_ids,
        'grade': grade_percentage,
        'total_score': total_score,
        'possible_score': total_grade,
        'total_grade': total_grade
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
