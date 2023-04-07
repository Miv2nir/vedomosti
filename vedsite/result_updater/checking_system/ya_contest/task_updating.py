import json
import pandas as pd
from ..protocol import TaskUpdater


class YaContestUpdater(TaskUpdater):
    def __init__(self, res_filepath, mapping):
        TaskUpdater.__init__(self, res_filepath, mapping)
        # self._user_mapping = mapping
        # self._new_res_table = self._read_new_results_file(res_filepath)

    def _read_new_results_file(self, path):
        try:
            csv = pd.read_csv(path, delimiter=",")
            csv = csv[csv.columns[2:-1]]
            csv["login"] = csv["login"].apply(lambda x: x.lower())
        except:
            input("Failed to open {}. Continue?".format(path))
            return None

        for i in range(1, len(csv.columns) - 1):
            csv[csv.columns[i]] = csv[csv.columns[i]].astype(str)
            # TODO: what kind of modification should be made if optimization is processed?
            csv[csv.columns[i]] = csv[csv.columns[i]].apply(lambda x: "1" if x[0] == "+" else "0")
        csv[csv.columns[1:-1]] = csv[csv.columns[1:-1]].astype(int)
        return csv

    def run(self, aggregator):
        if self._new_res_table is None:
            return None

        res = {}
        for group in self._user_mapping:
            res[group] = {}
            for login in self._user_mapping[group]:
                if login.lower() not in self._new_res_table["login"].values:
                    res[group][self._user_mapping[group][login]] = max(res[group].get(self._user_mapping[group][login],
                                                                                      0),
                                                                       0)
                    continue
                sub = self._new_res_table[self._new_res_table["login"] == login.lower()].values[0, 1:]
                res[group][self._user_mapping[group][login]] = aggregator.aggregate(sub)
        return res
