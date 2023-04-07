

class StudentListWrapperProtocol:
    def __init__(self, filename):
        self.filename = filename
        self._stud_list = self._open()

    def _open(self):
        raise NotImplementedError

    def get_students(self, grp_name, with_logins=True):
        raise NotImplementedError

    def add_student(self, grp_name, stud_name, logins=None):
        raise NotImplementedError

    def set_student_login(self, grp_name, stud_name, check_system, login):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def __getitem__(self, item):
        raise NotImplementedError
