from django.db import models
from django.conf import settings
from django.utils.timezone import now

# Existing Course and Lesson models are assumed to be above this block

class Question(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=1)

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).values_list('id', flat=True)
        return set(all_answers) == set(selected_ids)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    time = models.DateTimeField(default=now)