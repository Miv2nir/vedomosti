from .models import Teacher, Discipline, DisciplineGroup
import openpyxl

# for dir deletion


def del_group(g_number, user):
    print("wow deleting", g_number)
    g = DisciplineGroup.objects.filter(g_owner=user, g_number=g_number)
    for o in g:
        o.delete()


def del_discipline(d_id, user):
    g = DisciplineGroup.objects.filter(g_owner=user, d_id=d_id)
    for o in g:
        print("wow deleting", o.g_number)
        o.delete()
    print("wow deleting", d_id)
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
