from django.shortcuts import render
from django.template.defaulttags import register
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import django_cryptography.fields as crypt
import requests
import json
import pathlib
import pandas as pd
import os
import re
import xlsx2html
from uuid import uuid4
from bs4 import BeautifulSoup
# for logins

from django.contrib.auth import authenticate, login, logout

from .models import Teacher, Discipline, DisciplineGroup
from .forms import AuthForm, RegisterForm, LogOutForm, CredentialsForm, DisciplineForm, GroupForm, DisciplineListForm, GroupListForm
import result_updater.checking_system.ya_contest as ya_contest
from .utils import *


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
# Create your views here.


def register_user(request):  # going to roughly repeat the login_user view as to the process is largely similar
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_login = form.cleaned_data['login']
            try:  # check for existing users
                user = User.objects.get(username=user_login)
                return render(request, 'demo/register.html', {'form': form, 'user_found': True})
            except:
                pass  # no existing user found, proceed
            user_password = form.cleaned_data['password']
            if user_password != form.cleaned_data['password_verify']:  # passwords did not match
                return render(request, 'demo/register.html', {'form': form, 'password_mismatch': True})
            user_email = form.cleaned_data['email']

            if (not user_login) or (not user_email) or (not user_password):  # in the case of whether some credentials have been skipped
                return render(request, 'demo/register.html', {'form': form, 'incomplete_form': True})

            user = User.objects.create_user(user_login, user_email, user_password)
            user.save()  # created the user
            if user is not None:  # login the newly created user
                print('New User Logging in '+user_login)  # for the tests
                login(request, user)
            return HttpResponseRedirect('/')
    else:  # prompt the form
        form = RegisterForm()
        if request.user.is_authenticated:  # if logged in, redirect to the main page
            return HttpResponseRedirect('/')
    return render(request, 'demo/register.html', {'form': form})


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


def work(request):

    if not request.user.is_authenticated:  # user not yet logged in
        return HttpResponseRedirect('/login/')
    # look up named entries for a logged in user
    lookup = Discipline.objects.filter(d_owner=request.user)

    # for item in lookup:
    # print(item.d_name)

    return render(request, 'demo/work.html', {'username': request.user, 'lookup': lookup})


def work_new(request):
    if not request.user.is_authenticated:  # user not yet logged in
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        form_new = DisciplineForm(request.POST)
        if form_new.is_valid():
            d = Discipline(d_id=uuid4(), d_name=form_new.cleaned_data['d_name'], d_owner=request.user)
            d.save()
            lookup = Discipline.objects.filter(d_owner=request.user)
            # print(form_new.cleaned_data['d_name'])
            # return render(request, 'demo/work.html', {'username': request.user, 'lookup': lookup})
            return HttpResponseRedirect('/work/')
    # look up named entries for a logged in user
    lookup = Discipline.objects.filter(d_owner=request.user)
    form_new = DisciplineForm()
    return render(request, 'demo/work_new.html', {'username': request.user, 'lookup': lookup, 'form': form_new})


@register.filter  # for being able to send dicts over to templates basically
def get_value(dictionary, key):
    return dictionary.get(key)


def work_manage(request):

    if not request.user.is_authenticated:  # user not yet logged in
        return HttpResponseRedirect('/login/')
    # look up named entries for a logged in user
    # lookup = Discipline.objects.filter(d_owner=request.user)
    lookup = Discipline.objects.filter(d_owner=request.user)
    l = []
    name_uuid = {}
    for i in lookup:
        l.append(i.d_name)
        name_uuid[i.d_name] = i.d_id

    if request.method == 'POST':
        forml = DisciplineListForm(request.POST, d_names=l)
        if forml.is_valid():
            for name in l:
                d = Discipline.objects.filter(d_owner=request.user, d_name=name)[0]
                print(d.d_name)
                if forml.cleaned_data['d_og_name_'+name] != d.d_name:
                    d.d_name = forml.cleaned_data['d_og_name_'+name]
                    print(forml.cleaned_data['d_og_name_'+name])
                    d.save()
                # print(forml.cleaned_data['d_og_name_'+i])
            return HttpResponseRedirect('/work/')

    # list of forms for each entry in the database

    forml = DisciplineListForm(d_names=l)
    '''
    for item in lookup:
        prefill = {'d_name': item.d_name}
        form_new = DisciplineListForm(prefill)
        print(prefill)
        formlist.append(form_new)
    '''

    return render(request, 'demo/work_manage.html', {'forml': forml, 'name_uuid': name_uuid})


def work_delete(request, d_id):
    if not request.user.is_authenticated:  # user not yet logged in
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        del_discipline(d_id, request.user)
        return HttpResponseRedirect('/work/manage/')
    d = Discipline.objects.filter(d_owner=request.user, d_id=d_id)[0]
    lookup = DisciplineGroup.objects.filter(d_id=d_id)
    l = []
    for i in lookup:
        l.append(i.g_number)
    return render(request, 'demo/work_delete.html', {'d_id': d_id, 'd_name': d.d_name, 'g_list': l})


def discipline(request, d_id):
    # get discipline
    d = Discipline.objects.filter(d_id=d_id)[0]
    lookup = DisciplineGroup.objects.filter(d_id=d_id)
    return render(request, 'demo/group.html', {'username': request.user, 'lookup': lookup, 'd_id': d_id, 'd_name': d.d_name})


def discipline_new(request, d_id):
    if not request.user.is_authenticated:  # user not yet logged in
        return HttpResponseRedirect('/login/')
    d = Discipline.objects.filter(d_id=d_id)[0]
    if request.method == 'POST':
        form_new = GroupForm(request.POST)
        if form_new.is_valid():
            g = DisciplineGroup(g_id=uuid4(), g_number=form_new.cleaned_data['g_number'], d_id=d_id, g_owner=request.user)
            g.save()
            lookup = Discipline.objects.filter(d_owner=request.user)
            # return render(request, 'demo/group.html', {'username': request.user, 'lookup': lookup, 'd_name': d.d_name})
            return HttpResponseRedirect('/work/'+str(d_id)+'/')
    lookup = DisciplineGroup.objects.filter(d_id=d_id)
    form_new = GroupForm()
    return render(request, 'demo/group_new.html', {'username': request.user, 'lookup': lookup, 'd_name': d.d_name, 'd_id': d_id, 'form': form_new})


def discipline_manage(request, d_id):

    if not request.user.is_authenticated:  # user not yet logged in
        return HttpResponseRedirect('/login/')
    # look up named entries for a logged in user
    # lookup = Discipline.objects.filter(d_owner=request.user)
    lookup = DisciplineGroup.objects.filter(d_id=d_id)
    l = []
    for i in lookup:
        l.append(i.g_number)

    if request.method == 'POST':
        forml = GroupListForm(request.POST, g_numbers=l)
        if forml.is_valid():
            for num in l:
                g = DisciplineGroup.objects.filter(g_owner=request.user, d_id=d_id, g_number=num)[0]
                print(g.g_number)
                if forml.cleaned_data['g_og_number_'+str(num)] != g.g_number:
                    g.g_number = forml.cleaned_data['g_og_number_'+str(num)]
                    print(forml.cleaned_data['g_og_number_'+str(num)])
                    g.save()
                # print(forml.cleaned_data['d_og_name_'+i])
            return HttpResponseRedirect('/work/'+str(d_id)+'/')
    forml = GroupListForm(g_numbers=l)
    return render(request, 'demo/group_manage.html', {'forml': forml, 'd_id': d_id})


def discipline_delete(request, d_id, g_number):
    if not request.user.is_authenticated:  # user not yet logged in
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        del_group(g_number, request.user)
        return HttpResponseRedirect('/work/'+str(d_id)+'/manage/')
    return render(request, 'demo/group_delete.html', {'g_number': g_number, 'd_id': d_id})


def table(request, d_id, g_number):
    if not request.user.is_authenticated:  # user not yet logged in
        return HttpResponseRedirect('/login/')

    print(pathlib.Path().resolve())
    # find a table dir, make one if absent
    p = pathlib.Path('./generated/'+str(d_id)+'/'+str(g_number))  # dir with tables
    if not p.is_dir():
        p.mkdir(parents=True, exist_ok=True)
    # convert xlsx to html, must be named as table.xlsx
    print(str(p)+'/table.xlsx')
    t = xlsx2html.xlsx2html(str(p)+'/table.xlsx')
    t.seek(0)
    # print(t.read())
    # get the body out of the html element
    soup = BeautifulSoup(t.read(), "lxml")
    # return HttpResponse(soup.body.table)
    print(len(re.findall("\"*!.*3\"", str(soup.body.table))))
    # fix column formatting by adding more spacing arguments
    soup.body.table.colgroup
    coln = len(re.findall("\"*!.*3\"", str(soup.body.table)))
    # replace style="width with style="min-width as it causes rendering issues
    for i in soup.body.table.colgroup.select('col'):
        # soup.body.table.colgroup.insert(3, soup.new_tag(str(i).replace("width", "min-width")[1:-2]))
        # print(str(i).replace("width", "min-width")[1:-2])
        i.extract()
    # regen col styles
    soup.body.table.colgroup.insert(0, soup.new_tag('col style="min-width: 172.8px"'))
    soup.body.table.colgroup.insert(1, soup.new_tag('col style="min-width: 172.8px"'))
    # soup.body.table.colgroup.insert(1, soup.new_tag('col style="min-width: 120px"'))
    for i in range(coln-2):
        soup.body.table.colgroup.insert(3, soup.new_tag('col style="min-width: 87.36px"'))

    return render(request, 'demo/table.html', {'username': request.user, 'd_id': d_id, 'g_number': g_number, 'xlsx': str(soup.body.table)})

# something for the following function down below


def _digest(j,  contest_id, teacher_name=''):
    jout = {'contest_ID': contest_id,
            'contest_students': {}}
    for i in range(len(j['items'])):  # add students
        student_name = j['items'][i]['participant']['participantName']
        # print(jout['contest_students'])
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
    df.to_csv(pth+'/static/generated/'+filename)


def credentials(request):  # /credentials page
    print("Retrieving some stuff")
    if request.method == 'POST':
        form_credentials = CredentialsForm(request.POST)
        if form_credentials.is_valid():
            # look up the corresponding teacher in database

            ya_login = form_credentials.cleaned_data['ya_login']
            ya_password = form_credentials.cleaned_data['ya_password']
            ya_id = form_credentials.cleaned_data['ya_id']
            # print(ya_login)  # haha leaking personal info

            ya_user = ya_contest.authorization.YaContestAuthorizer(authorize=False)  # create an authorizer object
            ya_user.authorize({"login": ya_login, "password": ya_password})  # authorize the user (should refresh the session hopefully)
            if not Teacher.objects.filter(linked_user=request.user.username):  # check if a teacher object exists in a DB already
                ya_object = Teacher(linked_user=request.user.username, yandex_login=ya_login)  # creates a Teacher object in case of absense
            else:
                ya_object = Teacher.objects.filter(linked_user=request.user.username)
            ya_object.ya_session = ya_user.get_session()
            # print(ya_object.ya_session)
            # ya_object.save()
            # apparently am unable to save the session so gonna retrieve everything in one go now
            filename = request.user.username+'_'+str(ya_id)+'.json'
            pth = str(pathlib.Path(__file__).parent)
            ya_get = ya_contest.fetching.YaContestUpdFetcher(ya_user.get_session(), {ya_id: [ya_id]}, "automatic", pth+'/static/generated/'+filename)
            ya_get.fetch_updates()

            with open(pth+'/static/generated/'+filename, 'r', encoding='utf8') as f:
                try:
                    j = _digest(json.load(f), ya_id)  # turns retrieved .json into a desired format
                except:  # incorrect json means server did not tolerate the request
                    return render(request, 'demo/credentials.html', {'form_credentials': form_credentials, 'changes_saved': False, 'relog_needed': False, 'crash': True})
            with open(pth+'/static/generated/processed_'+filename, 'w', encoding='utf8') as f:
                f.write(json.dumps(j, ensure_ascii=False))
                print(pth+'/static/generated/processed_'+filename)
                os.remove(pth+'/static/generated/'+filename)  # no longer needed
            _json_to_csv(pth+'/static/generated/processed_'+filename, filename[:-5]+'.csv', pth)  # make a csv variant of the data
            with open(pth+'/static/generated/'+filename[:-5]+'.csv', 'r', encoding='utf8') as f:  # fixing up the csv lol
                deeta = f.readlines()
                deeta[0] = 'contest_students,contest_ID,results\n'
            with open(pth+'/static/generated/'+filename[:-5]+'.csv', 'w', encoding='utf8') as f:
                f.writelines(deeta)
            # purge old files
            purgetemplate = ['processed_'+filename, filename[:-5]+'.csv']
            print("current filename is ", filename)
            for purgename in os.listdir(pth+'/static/generated/'):
                # (purgename in purgetemplate) != (request.user.username in purgename)
                print(purgetemplate, purgename, ya_login, (request.user.username in purgename) and not (str(ya_id) in purgename))
                if (request.user.username in purgename) and not (str(ya_id) in purgename):
                    os.remove(pth+'/static/generated/'+purgename)

            return render(request, 'demo/credentials.html', {'form_credentials': form_credentials, 'changes_saved': True, 'relog_needed': False, 'pathcsv': ('/static/generated/'+filename[:-5]+'.csv'), 'pathjson': ('/static/generated/processed_'+filename)})
        else:
            form_credentials = CredentialsForm()
            return render(request, 'demo/credentials.html', {'form_credentials': form_credentials, 'changes_saved': False, 'relog_needed': False})
    else:
        form_credentials = CredentialsForm()
        return render(request, 'demo/credentials.html', {'form_credentials': form_credentials, 'changes_saved': False, 'relog_needed': False})
