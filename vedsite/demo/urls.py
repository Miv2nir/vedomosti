from django.urls import path
from django.views.static import serve
from django.conf import settings
from django.urls import re_path
import vedsite.settings
import pathlib
from . import views

urlpatterns = [
    re_path(
        r'^statics/(?P<path>.*)$',
        serve,
        {
            'document_root': settings.STATIC_URL,
            'show_indexes': True,  # must be True to render file list
        },
    ),

    path('', views.main_page, name='main'),
    path('work/', views.work, name='work'),
    path('work/new/', views.work_new, name='work_new'),
    path('work/manage/', views.work_manage, name='work_manage'),
    # dashboard!
    path('work/<uuid:d_id>/', views.discipline, name='discipline'),
    path('work/<uuid:d_id>/new/', views.discipline_new, name='discipline_new'),
    path('work/<uuid:d_id>/manage/', views.discipline_manage, name='discipline_manage'),
    path('work/<uuid:d_id>/<int:g_number>/', views.group, name='group'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('credentials/', views.credentials, name='credentials')
]
