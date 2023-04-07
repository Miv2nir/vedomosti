import json
from ..student_list import StudentListWrapperProtocol


class FormBackendProtocol:
    def __init__(self, engine):
        self.engine = engine

    # I/O

    def open(self, path):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def create(self, path):
        raise NotImplementedError

    # sheets and cells

    def select_sheet(self, sheet_name):
        raise NotImplementedError

    def get_cell_value(self, cell_addr):
        raise NotImplementedError

    def set_cell_value(self, cell_addr, value):
        raise NotImplementedError

    def set_cell_color(self, cell_addr, color):
        raise NotImplementedError

    # rows

    def insert_row(self, ind):
        raise NotImplementedError

    # def copy_cell(self, cell0, cell1):
    #     raise NotImplementedError

    def __getitem__(self, item):
        return self.get_cell_value(item)

    def __setitem__(self, key, value):
        return self.set_cell_value(key, value)


class FormWrapperProtocol:
    def __init__(self,
                 form_filepath,
                 task_blocks,
                 student_list_engine: StudentListWrapperProtocol,
                 sheets_engine: FormBackendProtocol
                 ):
        # self._filename = form_filepath
        # self._student_mapping_file_path = student_mapping_file_path
        # with open(self._student_mapping_file_path) as f:
        #     self._mapping = json.loads(f.read())["students"]
        self._student_list = student_list_engine
        self._engine = sheets_engine
        self._engine.open(form_filepath)
        self._blocks = task_blocks

    """
        SERVICE FUNCTIONS
    """

    def get_students(self, gr_ind, return_gropnames=False):
        # return self._mapping
        return self._student_list.get_students(gr_ind)

    def get_task_blocks(self):
        return self._blocks

    def save(self):
        self._engine.save()
        self._student_list.save()

    def to_html(self, sheet_num):
        raise NotImplementedError("This method must be overridden!")

    """
        UPDATE DO / UNDO FUNCTIONS
    """

    def add_updates(self, task_files, block_info):
        raise NotImplementedError("This method must be overridden!")

    """
        META UPDATE FUNCTIONS
    """

    def add_student(self, group_name, name, check_system_logins):
        raise NotImplementedError("This method must be overridden!")

