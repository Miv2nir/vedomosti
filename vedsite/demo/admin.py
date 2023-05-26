from django.contrib import admin

from .models import Teacher, Discipline, DisciplineGroup
admin.site.register(Teacher)
admin.site.register(Discipline)
admin.site.register(DisciplineGroup)
