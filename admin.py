from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'grade', 'lesson']

class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'course']

# Register models with their custom Admin interfaces
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)