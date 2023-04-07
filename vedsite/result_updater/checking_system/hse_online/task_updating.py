# coding=utf-8
import json
import pandas as pd
from ..protocol import TaskUpdater

class HSEOnlineTaskUpdater(TaskUpdater):
    def __init__(self, res_filepath, mapping):
        TaskUpdater.__init__(self, res_filepath, mapping)
        # self._user_mapping = mapping
        # self._new_res_table = self._read_new_results_file(res_filepath)
        # print(self._new_res_table)

    def _read_new_results_file(self, path):
        csv = pd.read_csv(path, delimiter=",")
        csv["Фамилия"] = csv["Фамилия"] + " " + csv["Имя Отчество"]
        cols = [col for col in csv.columns if col in ["Фамилия", "Оценка/100,00"]]
        csv = csv[cols]
        # csv["Оценка/100,00"] = csv["Оценка/100,00"].astype(float)
        # csv = csv[csv.columns[2:-1]]
        # for i in range(1, len(csv.columns) - 1):
        #     csv[csv.columns[i]] = csv[csv.columns[i]].astype(str)
        #     csv[csv.columns[i]] = csv[csv.columns[i]].apply(lambda x: "1" if x[0] == "+" else "0")
        # csv[csv.columns[1:-1]] = csv[csv.columns[1:-1]].astype(int)
        return csv

    def run(self, aggregator):
        res = {}
        for group in self._user_mapping:
            res[group] = {}
            for login in self._user_mapping[group]:
                if login not in self._new_res_table["Фамилия"].values:
                    res[group][self._user_mapping[group][login]] = 0
                    continue
                sub = self._new_res_table[self._new_res_table["Фамилия"] == login].values[0, 1:]
                # print(self._new_res_table[self._new_res_table["login"] == login])
                res[group][self._user_mapping[group][login]] = aggregator.aggregate(sub)
        return res
