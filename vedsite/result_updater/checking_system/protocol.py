
class Authorizer:
    def __init__(self, authorize=True):
        pass

    def authorize(self, credentials):
        raise Exception("Not implemented!")

    def get_token(self):
        raise Exception("Not implemented!")

    def logout(self):
        raise Exception("Not implemented!")


class CourseUpdateFetcher:
    def __init__(self):
        pass

    def fetch_updates(self):
        raise Exception("Not implemented!")


class TaskUpdater:
    def __init__(self, res_filepath, mapping):
        self._user_mapping = mapping
        self._new_res_table = self._read_new_results_file(res_filepath)

    def run(self, aggregator):
        raise Exception("Not implemented!")

    def _read_new_results_file(self, path):
        raise Exception("Not implemented!")