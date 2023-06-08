
from .authorization import Authorizer
import json
import requests as req
# import constants
from .constants import *
import pandas as pd
from ..protocol import CourseUpdateFetcher


class YaContestUpdFetcher(CourseUpdateFetcher):
    _token = None

    def __init__(self, session, task_ids, check_type, filename_template):
        # self._authorizer = Authorizer(APP_ID, auth_token_path)
        CourseUpdateFetcher.__init__(self)
        self._session = session
        self._task_ids = task_ids
        self._check_type = check_type
        self._name_template = filename_template

        # if not self._authorizer.update_authorization():
        #     raise Exception("Replace cookies manually!")

    def fetch_updates(self):
        paths = {}
        if self._check_type == "automatic":
            for cont_name in self._task_ids:
                paths[cont_name] = self._fetch_contest_results(self._task_ids[cont_name][0])
        else:
            raise Exception(f"Check type \"{self._check_type}\" not supported by {type(self).__name__}!")
        return paths

    def _fetch_contest_results(self, task_id):
        uri = "https://admin.contest.yandex.ru/api/contests/{}/submission?filter=".format(task_id)
        # uri = "https://admin.contest.yandex.ru/api/contest/{}/monitor/csv".format(task_id)

        # uri = "https://contest.yandex.ru/admin/contest-submissions/get-standings-csv?contestId={}".format(contest_id)
        # uri = "https://admin.contest.yandex.ru/contests"
        # headers = {# "Authorization": "{} {}".format("bearer",
        #            #                                 self._token),
        #     "Cookie": self._token,
        #     "Accept": "text/static,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        # }
        # r = req.get(uri, headers=headers)
        r = self._session.get(uri)
        # print(r.content)
        # input("c?")
        # print(r.history)
        # input('c?')
        if r.status_code != 200:
            print(uri)
            print(r.text)
            # raise Exception("Failed to open!")
            # input("Failed to fetch contest {}. Continue?".format(task_id))

        # input("c?")
        open(self._name_template.format(task_id),
             'wb').write(r.content)
        # return self._name_template.format(task_id)
        # yandex_df = pd.DataFrame(r.content)
        print(r.text)
        pd.DataFrame(json.loads(r.content)).to_csv("result.csv", index=False)
        print(yandex_df.columns.values.tolist())
        # return r.content  # file generation is unnecessary
        yandex_final = {"full_name": [], "contest_title": "contest {}".format(task_id), "checking_system_name": "Yandex",
                        "color": "FFEB9C"}
        all_tasks = {}
        for item in r.content["items"]:
            all_tasks.setdefault(item["problem"]["title"], [])
            if item["verdict"] == "OK":
                all_tasks[item["problem"]["title"]].append(item["participant"]["participantName"])
        # print(all_tasks)
        for task in all_tasks:
            yandex_final["full_name"].append(dict().fromkeys(task, all_tasks[task]))
        # print(yandex_final)
        return yandex_final


# if __name__ == "__main__":
#     CourseUpdFetcher("token.json", [], "")._fetch_contest_results(18983)
