from .authorization import Authorizer
import json
import requests as req
# import constants
from .constants import *
import pandas as pd
from ..protocol import CourseUpdateFetcher

class StepikUpdFetcher(CourseUpdateFetcher):
    _token = None

    def __init__(self, session, task_ids, check_type, filename_template):
        # self._authorizer = Authorizer(APP_ID, auth_token_path)
        CourseUpdateFetcher.__init__(self)
        self._session = session
        self._task_ids = task_ids
        self._check_type = check_type
        self._name_template = filename_template

    def fetch_updates(self):
        paths = {}
        if self._check_type == "automatic":
            for cont_name in self._task_ids:
                paths[cont_name] = self._fetch_contest_results(self._task_ids[cont_name][0])
        else:
            raise Exception(f"Check type \"{self._check_type}\" not supported by {type(self).__name__}!")
        return paths

    #def _fetch_contest_results(self, task_id):