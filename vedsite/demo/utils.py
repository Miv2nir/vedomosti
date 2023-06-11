from .models import *
import openpyxl
import shutil
import pickle
import requests
import pathlib
import result_updater.form_backend.excel.backend as bck
import result_updater.checking_system.ya_contest.authorization as yauth
import result_updater.checking_system.ya_contest.fetching as yfetch
import result_updater.checking_system.stepik.authorization as sauth
import result_updater.checking_system.stepik.fetching as sfetch
# for dir deletion


def del_group(g_number, d_id, user):
    print("wow deleting", g_number)
    g = DisciplineGroup.objects.filter(g_owner=user, d_id=d_id, g_number=g_number)
    # delete all belonging students
    s = Student.objects.filter(g_owner=user, d_id=d_id, g_number=g_number)
    for i in s:
        s.delete()
    for o in g:
        shutil.rmtree('generated/'+str(d_id)+'/'+str(g_number))
        o.delete()


def del_discipline(d_id, user):
    g = DisciplineGroup.objects.filter(g_owner=user, d_id=d_id)
    # delete all belonging students
    s = Student.objects.filter(s_owner=user, d_id=d_id)
    for i in s:
        s.delete()
    for o in g:
        print("wow deleting", o.g_number)
        o.delete()
    print("wow deleting", d_id)
    shutil.rmtree('generated/'+str(d_id))
    d = Discipline.objects.filter(d_owner=user, d_id=d_id)
    d.delete()


# for defaulting for a first sheet in xlsx


def table_set_first_sheet(table_dir, table_name='table.xlsx', table_result_name='tablecache.xlsx'):
    wb = openpyxl.load_workbook(table_dir+'/'+table_name, data_only=True)
    wb.active = wb[wb.get_sheet_names()[0]]
    wb.save(table_dir+'/'+table_result_name)


def table_clear_empty_rows(table_dir, table_name='table.xlsx', table_result_name='tablecache.xlsx'):
    wb = openpyxl.load_workbook(table_dir+'/'+table_name, data_only=True)
    ws = wb.active
    index = []
    for i in range(len(tuple(ws.rows))):
        f = False
        for cell in tuple(ws.rows)[i]:
            if cell.value != None:
                f = True
                break
        if not f:
            index.append(i)
    index.sort()
    for i in range(len(index)):
        ws.delete_rows(idx=index[i]+1-i)
    wb.save(table_dir+'/'+table_result_name)

# leftovers from a deprecated ye olde yandex puller


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


def student_name_interface(d_id, g_number, mode=''):
    l = []
    grps = Student.objects.filter(d_id=d_id, g_number=g_number)
    for i in grps:
        if not mode:
            l.append(i.s_display_name)
        if mode == 'yandex':
            l.append(i.s_ya_name)
        if mode == 'stepik':
            l.append(i.s_stepik_name)
        if mode == 'all':
            l.append([i.s_display_name, i.s_email, i.s_ya_name, i.s_stepik_name])
    return l


def write_cookies(cookie_dir, user, session):
    with open(str(cookie_dir)+'/ya_'+user, 'wb') as f:
        pickle.dump(session.cookies, f)


def read_cookies(cookie_dir, user):
    with open(str(cookie_dir)+'/ya_'+user, 'rb') as f:
        session = requests.Session()
        session.cookies = pickle.load(f)
    return session


def fill_table(user, source, task_id, d_id, g_number, table_path):
    # retrieve names
    l = []
    lookup = Student.objects.filter(s_owner=user, d_id=d_id, g_number=g_number)
    if source == 'yandex':
        for o in lookup:
            if o.s_ya_name:
                l.append(o.s_ya_name)
        yuser = yauth.YaContestAuthorizer(authorize=False)
        # yuser._session = requests.Session()
        yuser._session = read_cookies(pathlib.Path('./generated/cookies'), user.username)
        ywork = yfetch.YaContestUpdFetcher(yuser.get_session(), task_id, "automatic", '{}.json')
        j = ywork._fetch_contest_results(task_id)
    elif source == 'stepik':
        for o in lookup:
            if o.s_stepik_name:
                l.append(o.s_stepik_name)
        # get things from db
        creds = Credentials.objects.filter(user_name=user)[0]
        d = {"client_id": creds.stepik_id, "client_secret": creds.stepik_key}
        suser = sauth.StepikAuthorizer()
        suser.authorize(d)
        sf = sfetch.StepikUpdFetcher(suser.get_token())
        j = sf._fetch_contest_results(task_id)
    # set thing in the table

    bck.CreateTable(l, table_path, data=j)
