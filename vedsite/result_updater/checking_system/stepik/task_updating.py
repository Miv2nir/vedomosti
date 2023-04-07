import pandas as pd
from ..protocol import TaskUpdater

class StepikUpdater(TaskUpdater):
    def __init__(self, res_filepath, mapping):
        TaskUpdater.__init__(self, res_filepath, mapping)
    # достать csv табличку и посмотреть точные данные

    #def _read_new_results_file(self, path):
        #csv = pd.read_csv(path, delimiter=",")
        #csv = csv[csv.columns[2:-1]]

    #def run(self, aggregator):