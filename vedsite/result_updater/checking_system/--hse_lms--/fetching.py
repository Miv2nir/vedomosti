
from .authorization import Authorizer
import json
import requests as req
# import constants
from .constants import *
import pandas as pd


class CourseUpdFetcher:
    _token = None

    def __init__(self, auth_token, contest_ids, filename_template):
        # self._authorizer = Authorizer()
        self._token = auth_token # self._authorizer.get_token()
        self._contest_ids = contest_ids
        self._name_template = filename_template

        # if not self._authorizer.update_authorization():
        #     raise Exception("Replace cookies manually!")

    def fetch_updates(self):
        paths = {}
        for cont_name in self._contest_ids:
            paths[cont_name] = self._fetch_contest_results(self._contest_ids[cont_name])
        return paths

    def _fetch_contest_results(self, contest_id):
        # uri = "https://admin.contest.yandex.ru/api/contest/{}/monitor/csv".format(contest_id)
        uri = "https://online.hse.ru/mod/quiz/report.php?download=csv&id={}&mode=overview&" \
              "attempts=enrolled_with&onlygraded=1&states=finished&onlyregraded=&slotmarks=1".format(contest_id)
        # uri = "https://admin.contest.yandex.ru/contests"
        headers = {
            "Cookie": self._token,
            "Accept": "text/static,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}
        r = req.get(uri, headers=headers)
        # print(r.content)
        # input("c?")
        if r.status_code != 200:
            print(r.content)
            raise Exception("Failed to open!")
        # input("c?")
        open(self._name_template.format(contest_id),
             'wb').write(r.content)
        return self._name_template.format(contest_id)


# if __name__ == "__main__":
#     CourseUpdFetcher("token.json", [], "")._fetch_contest_results(18983)
