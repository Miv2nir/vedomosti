from .__protocol import StudentListWrapperProtocol
import pandas as pd
import numpy as np


class CSVStudentList(StudentListWrapperProtocol):
    def __init__(self, filename):
        super().__init__(filename)

    def _open(self):
        return pd.read_csv(self.filename)

    def save(self):
        self._stud_list.to_csv(self.filename)

    def get_students(self, grp_name, with_logins=True):
        tgt_cols = ["student"]
        if with_logins:
            tgt_cols += self._stud_list.columns[self._stud_list.columns.tolist().index("student") + 1:]
        stud_list = self._stud_list[self._stud_list["group"] == grp_name]

        if with_logins:
            stud_list = stud_list[tgt_cols]
            return stud_list

        return sorted(np.unique(stud_list["student"]))

    def add_student(self, grp_name, stud_name, logins=None):
        app_row = {"group": grp_name, "student": stud_name}
        if logins is None:
            logins = {}
        for check_sys in self._stud_list.columns[self._stud_list.columns.tolist().index("student") + 1:]:
            if check_sys in logins:
                app_row[check_sys] = logins[check_sys]
            else:
                app_row[check_sys] = "-1"
        self._stud_list = self._stud_list.append(app_row)
        # self.save()

    def set_student_login(self, grp_name, stud_name, check_system, login):
        stud_rows = self._stud_list[self._stud_list["student"] == stud_name]
        if stud_rows.shape[0] == 0:
            raise ValueError("No student found in list!")

        prev_check_sys_logins = stud_rows[check_system].values
        if login in prev_check_sys_logins:
            # MARK: by now - ignore.
            return

        if "-1" in prev_check_sys_logins:
            row_i_to_insert = np.where(prev_check_sys_logins == "-1")[0][0]
            row_i_to_insert = stud_rows.index[row_i_to_insert]
            self._stud_list.loc[row_i_to_insert][check_system] = login
        else:
            self.add_student(grp_name, stud_name, logins={check_system: login})

        # self.save()

    def __getitem__(self, item):
        df = self._stud_list[["group", "student", item]]
        ans = {}
        for row in df.values:
            if row[2] == "-1":
                continue
            if row[0] not in ans:
                ans[row[0]] = {}
            ans[row[0]][row[2]] = row[1]
        return ans
