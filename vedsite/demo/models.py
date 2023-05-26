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


class Discipline(models.Model):
    d_id = models.UUIDField()
    d_name = models.CharField(max_length=200)
    d_owner = models.CharField(max_length=200)
    # d_children = models.CharField(max_length=200)

    def __str__(self):
        return "Discipline " + self.d_name+" of "+self.d_owner

    class Meta:
        verbose_name = "Discipline"
        verbose_name_plural = "Disciplines"


class DisciplineGroup(models.Model):
    g_id = models.UUIDField()
    g_number = models.IntegerField()
    # parent Discipline ID
    d_id = models.UUIDField()

    def __str__(self):
        return "Group " + str(self.g_number)+" of "+str(self.d_id)

    class Meta:
        verbose_name = "Student Group"
        verbose_name_plural = "Student Groups"


class Students(models.Model):
    s_id = models.UUIDField()
    s_name = models.CharField(max_length=200)
    s_email = models.CharField(max_length=2000)
    # parent Group ID
    g_id = models.UUIDField()
    g_number = models.IntegerField()


'''
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

'''
