from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Enrollment, Question, Choice, Submission

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)

    if request.method == 'POST':
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Collect selected choice IDs from POST request
        selected_choice_ids = []
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                selected_choice_ids.append(int(value))

        selected_choices = Choice.objects.filter(id__in=selected_choice_ids)
        submission.choices.set(selected_choices)

        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)
    
    return redirect('onlinecourse:course_details', course_id=course.id)


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_choices = submission.choices.all()
    selected_ids = [c.id for c in selected_choices]

    total_score = 0
    earned_score = 0

    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            total_score += question.grade
            if question.is_get_score(selected_ids):
                earned_score += question.grade

    grade_percentage = int((earned_score / total_score) * 100) if total_score > 0 else 0

    context = {
        'course': course,
        'selected_ids': selected_ids,
        'grade': grade_percentage,
        'submission': submission,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
