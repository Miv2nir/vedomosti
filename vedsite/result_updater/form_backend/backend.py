from .__protocol import FormWrapperProtocol
from ..checking_system import *
from .color_constants import *


class Gradebook(FormWrapperProtocol):
    def __init__(self,
                 form_filepath,
                 task_blocks,
                 student_list_engine,
                 sheets_engine):
        super().__init__(form_filepath,
                         task_blocks,
                         student_list_engine,
                         sheets_engine)

    # def get_students(self, gr_ind, return_groupnames=False):
    #     reverse_mapping = {}
    #     all_students = []
    #     # group_name = list(self._mapping[list(self._mapping.keys())[-1]].keys())[gr_ind]
    #     group_name = list(list(self._mapping.values())[0].keys())[gr_ind]
    #     for system_name in self._mapping:
    #         if group_name not in self._mapping[system_name]:
    #             reverse_mapping[system_name] = {}
    #             continue
    #         reverse_mapping[system_name] = {v: k for k, v in self._mapping[system_name][group_name].items()}
    #         all_students += list(self._mapping[system_name][group_name].values())
    #     all_students = sorted(list(set(all_students)))
    #     data = [["Студент"] + list(reverse_mapping.keys())]
    #     for stud in all_students:
    #         stud_data = [stud]
    #         for system_name in reverse_mapping:
    #             if stud in reverse_mapping[system_name]:
    #                 stud_data += [reverse_mapping[system_name][stud]]
    #             else:
    #                 stud_data += ["---"]
    #         data += [stud_data]
    #     if return_groupnames:
    #         return data, list(list(self._mapping.values())[0].keys())
    #     return data

    def get_task_blocks(self):
        return self._blocks

    def to_html(self, sheet_num):
        raise NotImplementedError

    def add_updates(self, task_files, block_info):
        def update_stud_task(grp_name, stud_list, task, upd_vals, col, st_row, cur_updates):
            cur_updates = cur_updates
            for i, k in enumerate(list(upd_vals.keys())):
                if upd_vals[k] == 0:
                    continue

                tgt_cell = col + str(st_row + stud_list.index(k))

                prev_val = self._engine[tgt_cell]
                prev_val = 0 if prev_val is None else prev_val

                if block_info["check_type"] == "manual":
                    if prev_val == 0:
                        self._engine.set_cell_color(tgt_cell, MANUAL_UPDATE_COLOR)
                        if k not in cur_updates[grp_name]:
                            cur_updates[grp_name][k] = {}
                        cur_updates[grp_name][k][task] = [prev_val, "givenin"]
                    continue

                new_val = upd_vals[k]
                if type(new_val) == str:
                    new_val = float(new_val.replace(",", "."))
                if new_val <= prev_val:
                    continue
                is_upd = prev_val != new_val

                if is_upd:
                    self._engine[tgt_cell] = new_val
                    if k not in cur_updates[grp_name]:
                        cur_updates[grp_name][k] = {}
                    cur_updates[grp_name][k][task] = [prev_val, new_val]
                    # TODO: set cell color
                    self._engine.set_cell_color(tgt_cell, AUTOMATIC_UPDATE_COLOR)

            return cur_updates

        def update_group(grp_name, task, upd_vals, cur_updates):
            cur_updates = cur_updates
            if grp_name not in cur_updates:
                updates[grp_name] = {}
            # select sheet from overall doc
            self._engine.select_sheet(grp_name)

            # TODO: do clear (if needed)
            starting_cell = block_info["tasks"][task][1]
            if starting_cell.__class__.__name__ == "list":
                starting_cell = starting_cell[0]
            starting_cell = starting_cell(len(self._student_list[block_info["system"]][grp_name]))
            st_row_ind = int(starting_cell[1:])
            col_letter = starting_cell[0]

            # FIXME: if local order of logins is the same as in the form,
            # FIXME:        this block can be ignored. Could lead to slight speedup
            form_students = []
            cur_cell = block_info["student_name_start_cell"]
            if cur_cell.__class__.__name__ == "function":
                cur_cell = cur_cell(len(self._student_list[block_info["system"]][grp_name]))
            while self._engine[cur_cell] is not None:
                # print(sheet[cur_cell].value)
                form_students += [self._engine[cur_cell]]
                cur_cell = cur_cell[0] + str(int(cur_cell[1:]) + 1)

            cur_updates = update_stud_task(grp_name, form_students,
                                           task, upd_vals,
                                           col_letter, st_row_ind,
                                           cur_updates)
            return cur_updates

        updates = {}

        for task_ind, task_name in enumerate(task_files.keys()):
            cont_res = get_task_updater_class(block_info["system"])(task_files[task_name],
                                                                    self._student_list[block_info["system"]]
                                                                    ).run(block_info["aggregator"])
            if cont_res is None:
                continue
            for group_name in cont_res.keys():
                update_group(group_name, task_name, cont_res[group_name], updates)

        return updates

    def add_student(self, group_name, name, check_system_logins):
        # self._engine.select_sheet(group_name)
        # grp_studs = sorted(self._mapping[group_name])
        self._student_list.add_student(group_name, name, check_system_logins)
        # TODO: add respective row in engine
