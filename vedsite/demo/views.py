from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth import authenticate
import django_cryptography.fields as crypt
import requests
import json
import pathlib
import pandas as pd
import os

# for logins

from django.contrib.auth import authenticate, login, logout

from .models import Teacher
from .forms import AuthForm, LogOutForm, CredentialsForm
import result_updater.checking_system.ya_contest as ya_contest


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
# Create your views here.


def login_user(request):
    if request.method == 'POST':  # look for the imports
        form = AuthForm(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data['login']
            user_password = form.cleaned_data['password']
            user = authenticate(username=user_login, password=user_password)

            if request.user.is_authenticated:  # if logged in, redirect to the main page
                return HttpResponseRedirect('/')

            if user is not None:  # accept the form and login the user
                print('Logging in '+user_login)  # for the tests
                login(request, user)
                return HttpResponseRedirect('/')
            else:  # failed credentials check
                form = AuthForm()
                return render(request, 'demo/login.html', {'form': form, 'failed_login': True})
    else:  # prompt the form
        form = AuthForm()
    return render(request, 'demo/login.html', {'form': form})


def logout_user(request):
    if request.user.is_authenticated:
        print('Logging out '+request.user.username)
        logout(request)
    return HttpResponseRedirect('/login/')


def main_page(request):
    if not request.user.is_authenticated:  # user not yet logged in
        return HttpResponseRedirect('/login/')
    form_logout = LogOutForm()
    return render(request, 'demo/main.html', {'username': request.user, 'form_logout': form_logout})

# something for the following function down below


def _digest(j,  contest_id, teacher_name=''):
    jout = {'contest_ID': contest_id,
            'contest_students': {}}
    for i in range(len(j['items'])):  # add students
        student_name = j['items'][i]['participant']['participantName']
        print(jout['contest_students'])
        if not (student_name in jout['contest_students']):  # check if an entry for a student is already present
            student = {
                j['items'][i]['problem']['title']: (j['items'][i]['verdict'] == 'OK')}
            jout['contest_students'][student_name] = student
        else:
            # print('hi')
            task_title = j['items'][i]['problem']['title']
            try:  # task titles match
                jout['contest_students'][student_name][task_title] = ((j['items'][i]['verdict'] == 'OK') or (jout['contest_students'][student_name][task_title]))  # logical or on whether the test has been passed or not before
            except KeyError:
                jout['contest_students'][student_name][task_title] = (j['items'][i]['verdict'] == 'OK')
    return jout


def _json_to_csv(json_string, filename, pth):
    df = pd.read_json(json_string)
    df.to_csv(pth+'/static/'+filename)


def credentials(request):  # /credentials page
    if request.method == 'POST':
        form_credentials = CredentialsForm(request.POST)
        if form_credentials.is_valid():
            # look up the corresponding teacher in database

            ya_login = form_credentials.cleaned_data['ya_login']
            ya_password = form_credentials.cleaned_data['ya_password']
            ya_id = form_credentials.cleaned_data['ya_id']
            print(ya_login)  # haha leaking personal info

            ya_user = ya_contest.authorization.YaContestAuthorizer(authorize=False)  # create an authorizer object
            ya_user.authorize({"login": ya_login, "password": ya_password})  # authorize the user (should refresh the session hopefully)
            if not Teacher.objects.filter(linked_user=request.user.username):  # check if a teacher object exists in a DB already
                ya_object = Teacher(linked_user=request.user.username, yandex_login=ya_login)  # creates a Teacher object in case of absense
            else:
                ya_object = Teacher.objects.filter(linked_user=request.user.username)
            ya_object.ya_session = ya_user.get_session()
            print(ya_object.ya_session)
            # ya_object.save()
            # apparently am unable to save the session so gonna retrieve everything in one go now
            filename = request.user.username+'_'+str(ya_id)+'.json'
            pth = str(pathlib.Path(__file__).parent)
            ya_get = ya_contest.fetching.YaContestUpdFetcher(ya_user.get_session(), {ya_id: [ya_id]}, "automatic", pth+'/static/'+filename)
            ya_get.fetch_updates()
            print(pth)
            with open(pth+'/static/'+filename, 'r', encoding='utf8') as f:
                try:
                    j = _digest(json.load(f), ya_id)  # turns retrieved .json into a desired format
                except:  # incorrect json means server did not tolerate the request
                    return render(request, 'demo/credentials.html', {'form_credentials': form_credentials, 'changes_saved': False, 'relog_needed': False, 'crash': True})
            with open(pth+'/static/processed_'+filename, 'w', encoding='utf8') as f:
                f.write(json.dumps(j, ensure_ascii=False))
                print(pth+'/static/processed_'+filename)
                # os.remove(pth+'/static/'+filename)  # no longer needed
            _json_to_csv(pth+'/static/processed_'+filename, filename[:-5]+'.csv', pth)  # make a csv variant of the data
            with open(pth+'/static/'+filename[:-5]+'.csv', 'r', encoding='utf8') as f:  # fixing up the csv lol
                deeta = f.readlines()
                deeta[0] = 'contest_students,contest_ID,results\n'
            with open(pth+'/static/'+filename[:-5]+'.csv', 'w', encoding='utf8') as f:
                f.writelines(deeta)

            return render(request, 'demo/credentials.html', {'form_credentials': form_credentials, 'changes_saved': True, 'relog_needed': False, 'pathcsv': ('/static/'+filename[:-5]+'.csv'), 'pathjson': ('/static/processed_'+filename)})
        else:
            form_credentials = CredentialsForm()
            return render(request, 'demo/credentials.html', {'form_credentials': form_credentials, 'changes_saved': False, 'relog_needed': False})
    else:
        form_credentials = CredentialsForm()
        return render(request, 'demo/credentials.html', {'form_credentials': form_credentials, 'changes_saved': False, 'relog_needed': False})
