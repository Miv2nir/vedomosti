from .models import Teacher, Discipline, DisciplineGroup


def del_group(g_number, user):
    print("wow deleting", g_number)
    g = DisciplineGroup.objects.filter(g_number=g_number)
    for o in g:
        o.delete()


def del_discipline(d_id, user):
    g = DisciplineGroup.objects.filter(d_id=d_id)
    for o in g:
        print("wow deleting", o.g_number)
        o.delete()
    print("wow deleting", d_id)
    d = Discipline.objects.filter(d_owner=user, d_id=d_id)
    d.delete()
