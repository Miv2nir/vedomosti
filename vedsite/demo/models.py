from django.db import models
from django.utils import timezone
import datetime


class Teacher(models.Model):
    linked_user = models.CharField(max_length=200)
    yandex_login = models.CharField(max_length=200, blank=True)
    yandex_session = models.CharField(max_length=200, blank=True)
    stepik_login = models.CharField(max_length=200, blank=True)
    stepik_password = models.CharField(max_length=200, blank=True)

    # to add hse api keys as well


class Student(models.Model):
    linked_teacher = models.CharField(max_length=200)
    tasks = models.JSONField(blank=True)


'''
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

'''
