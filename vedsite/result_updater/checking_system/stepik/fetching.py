from .authorization import Authorizer
import json
import requests
# import constants
from .constants import *
import pandas as pd
from ..protocol import CourseUpdateFetcher


class StepikUpdFetcher(CourseUpdateFetcher):
    _token = None

    def __init__(self, token):
        # self._authorizer = Authorizer(APP_ID, auth_token_path)
        CourseUpdateFetcher.__init__(self)
        self._token = token

#    def fetch_updates(self):
#        paths = {}
#        if self._check_type == "automatic":
#            for cont_name in self._task_ids:
#                paths[cont_name] = self._fetch_contest_results(self._task_ids[cont_name][0])
#        else:
#            raise Exception(f"Check type \"{self._check_type}\" not supported by {type(self).__name__}!")
#        return paths

    # def _fetch_contest_results(self, task_id):

    def _fetch_contest_results(self, task_id):
        # print("Hi!")
        headers = {'Authorization': 'Bearer '+self._token}
        # stepik_final = {"full_name": [], "checking_system_name": "Stepik", "color": "C6EFCE"}
        stepik_final = {"full_name": [], "contest_title": "contest {}".format(task_id), "checking_system_name": "Stepik", "color": "C6EFCE"}
        all_steps = []
        all_attempts = []
        all_users = []
        # all_names = []
        count = 0
        # names_copy = []

        uri = "https://stepik.org/api/steps?lesson={}".format(task_id)
        st_unit = requests.get(uri, headers=headers).json()
        # print(st_unit)
        # берём из step (contest) submissions
        if len(st_unit['steps']) == 0:
            raise KeyError("Unable to parse stepik")
        for UnitToStep in st_unit["steps"]:
            # print('st_unit["steps"]', UnitToStep)
            all_steps.append(UnitToStep["id"])
        for step in all_steps:
            # all_names.clear()
            # print('all_steps', step)
            urls = "https://stepik.org/api/submissions?order=asc&page=1&status=correct&step={}".format(step)
            page = 2

            # пока есть attempts на нескольких страничках
            while True:
                # print('True')
                st_steps = requests.get(urls, headers=headers).json()

            # берём из submissions attempt
                for StepToAttempt in st_steps["submissions"]:
                    # print(StepToAttempt["attempt"])
                    all_attempts.append("ids%5B%5D={}".format(StepToAttempt["attempt"]) + "&")

                # есть ли submissions
                if not st_steps["meta"]["has_next"]:
                    break

                urls = "https://stepik.org/api/submissions?order=asc&page={}".format(page) + "&status=correct&step={}".format(step)
                page += 1

            if len(all_attempts) == 0:
                # continue
                raise KeyError("Unable to parse stepik")

            # print(len(all_attempts))

            # создаём url
            urla_json = "https://stepik.org/api/attempts?"
            for num in all_attempts:
                # print('all_attempts', num)
                urla_json += num
            # print(urla_json)
            st_attempts = requests.get(urla_json, headers=headers).json()

            # достаём user
            for AttemptToUser in st_attempts["attempts"]:
                # print('st_attempts["attempts"]', AttemptToUser)
                all_users.append("ids%5B%5D={}".format(AttemptToUser["user"]) + "&")
            # создаём url
            urlu_json = "https://stepik.org/api/users?"
            for num in all_users:
                # print('all_users', num)
                urlu_json += num
            st_users = requests.get(urlu_json, headers=headers).json()
            # print(st_users)
            # берём имя user
            stepik_final["full_name"].append({str(step): []})
            for at in st_users["users"]:
                # print('st_users["users"]', at)
                stepik_final["full_name"][count][str(step)].append(at["full_name"])
                # print(at["full_name"])
            # names_copy = all_names
            # print(stepik_final["full_name"][0])
            stepik_final["full_name"][count][str(step)].sort()
            all_attempts.clear()
            all_users.clear()
            print("processing stepik(takes a while)", len(stepik_final["full_name"][count][str(step)]))
            print(stepik_final["full_name"][count][str(step)])
            count += 1
        return stepik_final
