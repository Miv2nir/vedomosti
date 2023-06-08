from ..__protocol import FormBackendProtocol
import openpyxl

from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.styles import Border, Side, PatternFill, Font, Alignment


def CreateTable(data, names):
    # C6EFCE - stepik
    # FFEB9C - yandex

    # print(len(names))
    # print(names)

    col = 3
    r = 3

    wb = Workbook()
    ws = wb.active
    ws.title = "Контесты"
    # print(wb.sheetnames)
    # ws.column_dimensions['A'].width = 36
    ws["A3"] = "Student"
    ws["A3"].alignment = Alignment(horizontal="center", vertical="center")
    for row in range(1, len(names) + 1):
        ws.cell(column=1, row=row + 3, value=names[row - 1])
    ws["B3"] = "Student email"

    ws.merge_cells(start_row=1, start_column=3, end_row=1, end_column=len(data["full_name"]) + 3)
    checking_system = ws['C1']
    checking_system.value = data["checking_system_name"]
    checking_system.alignment = Alignment(horizontal="center", vertical="center")
    checking_system.fill = PatternFill("solid", fgColor=data["color"])
    checking_system.font = Font(bold=True, name='Sans', size=16)

    ws.merge_cells(start_row=2, start_column=3, end_row=2, end_column=len(data["full_name"]) + 3)
    contest_name = ws['C2']
    contest_name.value = data["contest_title"]
    contest_name.alignment = Alignment(horizontal="center", vertical="center")
    contest_name.font = Font(bold=False, name='Sans', size=14)

    steps = []
    for step in data["full_name"]:
        steps.append(*step.keys())

    # steps = [int(x) for x in steps]
    # print(len(steps))

    for step in range(3, len(data["full_name"]) + 3):
        ws.cell(column=step, row=3, value=steps[step - 3])
    ws.cell(column=len(data["full_name"]) + 3, row=3).value = "Score"
    ws.cell(column=len(data["full_name"]) + 3, row=3).alignment = Alignment(horizontal="center", vertical="center")

    for i in range(len(names)):
        for j in range(len(data["full_name"])):
            ws.cell(column=j + 3, row=i + 4, value=0)

    # for name in data["full_name"]:
    # print(len(name))
    # print(name)
    # for stud in name.values():
    # print(stud)
    # for full_name in stud:
    # r += 1
    # print(len(stud))
    # ws.cell(column = col, row = r, value = 0)
    # print(full_name, r, cnt)
    # print(col)
    # col += 1
    # r = 3
    # print('здесь')

    cnt = 0
    for name in data["full_name"]:
        for stud in name.values():
            if len(stud) == 0:
                continue
            for n in range(len(names)):
                # print(n, len(names))
                r += 1
                if names[n] == stud[cnt]:
                    ws.cell(column=col, row=r, value=1)
                    cnt += 1
            col += 1
            r = 3
            cnt = 0

    for rows in range(len(names)):
        score = 0
        for columns in range(len(data["full_name"])):
            score += ws.cell(row=rows + 4, column=columns + 3).value
        # print(row)
        # print(score)
        ws.cell(row=rows + 4, column=len(data["full_name"]) + 3, value=score)

    wb.save(contest_name.value + '.xlsx')

    return 0


class ExcelBackend(FormBackendProtocol):
    def __init__(self):
        super().__init__(None)

    def open(self, path):
        self._filename = path
        self._form = openpyxl.load_workbook(filename=path)
        self._const_form = openpyxl.load_workbook(filename=path,
                                                  data_only=True
                                                  )
        self._sheet = None
        self._val_sheet = None

    def save(self):
        from datetime import datetime
        date = datetime.date(datetime.now())
        filename = str(self._filename)  # "/".join(self._filename.split(".")[:-1]) + "_" + str(date) + ".xlsx"
        self._const_form.close()
        self._form.save(filename)

    def create(self, path):
        wb = openpyxl.Workbook()
        wb.save(path)
        wb.close()
        del wb
        self.open(path)

    def select_sheet(self, sheet_name):
        self._sheet = self._form[sheet_name]
        self._val_sheet = self._const_form[sheet_name]

    def get_cell_value(self, cell_addr):
        return self._val_sheet[cell_addr].value

    def set_cell_value(self, cell_addr, value):
        self._sheet[cell_addr] = value
        self._val_sheet[cell_addr] = value

    def set_cell_color(self, cell_addr, color):
        c = openpyxl.styles.colors.Color(rgb=color)
        self._sheet[cell_addr].fill = openpyxl.styles.fills.PatternFill(patternType='solid',
                                                                        start_color=c)

    def insert_row(self, ind):
        self._sheet.insert_row(ind)
        self._val_sheet.insert_row(ind)
