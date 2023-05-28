from .authorization import Authorizer
import json
import requests
# import constants
from .constants import *
import pandas as pd
from ..protocol import CourseUpdateFetcher


def stepik_json(stepik_data):
    with open("stepik.json", "w") as fh:
        json.dump(stepik_data, fh)

    with open("stepik.json", "r") as fh:
        stepik_result = json.load(fh)
    return stepik_result


class StepikUpdFetcher(CourseUpdateFetcher):
    _token = None

    def __init__(self, session, token):
        # self._authorizer = Authorizer(APP_ID, auth_token_path)
        CourseUpdateFetcher.__init__(self)
        self._session = session
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
        print("Hi!")
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36",
                   }
        stepik_final = {"full_name": []}
        all_steps = []
        all_attempts = []
        all_users = []
        all_names = []

        uri = "https://stepik.org/api/steps?lesson={}".format(task_id)
        uri_json = self._session.get(uri, headers=headers).json()
        st_unit = stepik_json(uri_json)
        # берём из step (contest) submissions
        for UnitToStep in st_unit["steps"]:
            print('st_unit["steps"]', UnitToStep)
            all_steps.append(UnitToStep["id"])
        for step in all_steps:
            print('all_steps', step)
            urls = "https://stepik.org/api/submissions?order=asc&page=1&status=correct&step={}".format(step)
            page = 2

            # пока есть attempts на нескольких страничках
            while True:
                print('True')
                s_json = self._session.get(urls, headers=headers).json()
                st_steps = stepik_json(s_json)

            # берём из submissions attempt
                for StepToAttempt in st_steps["submissions"]:
                    print('True')
                    all_attempts.append("ids%5B%5D=".format(StepToAttempt["attempt"]) + "&")

                # есть ли submissions
                if not st_steps["meta"]["has_next"]:
                    break

                urls = "https://stepik.org/api/submissions?order=asc&page={}".format(page) + "&status=correct&step={}".format(step)
                page += 1

            # создаём url
            urla_json = "https://stepik.org/api/attempts?"
            for num in all_attempts:
                print('all_attempts', num)
                urla_json += all_attempts[num]

            a_json = self._session.get(urla_json, headers=headers).json()
            st_attempts = stepik_json(a_json)

            # достаём user
            for AttemptToUser in st_attempts["attempts"]:
                print('st_attempts["attempts"]', AttemptToUser)
                all_users.append("ids%5B%5D=".format(AttemptToUser["user"]) + "&")
            # создаём url
            urlu_json = "https://stepik.org/api/users?"
            for num in all_users:
                print('all_users', num)
                urlu_json += all_users[num]
            u_json = self._session.get(urla_json, headers=headers).json()
            st_users = stepik_json(u_json)

            # берём имя user
            for at in st_users["users"]:
                print('st_users["users"]', at)
                all_names.append(at["full_name"])

            stepik_final["full_name"].append({step: all_names})
        return stepik_final
