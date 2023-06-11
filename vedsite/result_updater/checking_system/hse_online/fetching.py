# coding=utf-8
from .authorization import Authorizer
import json
import requests as req
# import constants
from .constants import *
from ..protocol import CourseUpdateFetcher
import pandas as pd
from bs4 import BeautifulSoup


class HSEOnlineTaskUpdFetcher(CourseUpdateFetcher):
    _token = None

    def __init__(self, session, task_ids, check_type, filename_template):
        # self._authorizer = Authorizer()
        CourseUpdateFetcher.__init__(self)
        self._session = session # self._authorizer.get_token()
        self._task_ids = task_ids
        self._name_template = filename_template
        self._check_type = check_type

        # if not self._authorizer.update_authorization():
        #     raise Exception("Replace cookies manually!")

    def fetch_updates(self):
        paths = {}
        if self._check_type == "automatic":
            for cont_name in self._task_ids:
                paths[cont_name] = self._fetch_auto_task_results(self._task_ids[cont_name][0])
        elif self._check_type == "manual":
            for cont_name in self._task_ids:
                paths[cont_name] = self._fetch_manual_task_results(self._task_ids[cont_name][0])
        return paths

    def _fetch_auto_task_results(self, task_id):
        uri = "https://online.hse.ru/mod/quiz/report.php?download=csv&id={}&mode=overview&" \
              "attempts=enrolled_with&onlygraded=1&states=finished&onlyregraded=&slotmarks=1".format(task_id)
        headers = {
            "Cookie": self._token,
            "Accept": "text/static,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}
        r = self._session.get(uri, headers=headers)
        if r.status_code != 200:
            print(r.content)
            raise Exception("Failed to open!")
        with open(self._name_template.format(task_id),'wb') as f:
            f.write(r.content)
        return self._name_template.format(task_id)

    def _fetch_manual_task_results(self, task_id):
        uri = "https://online.hse.ru/mod/assign/view.php?id={}&action=grading".format(task_id)
        headers = {
            "Cookie": self._token,
            "Accept": "text/static,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}
        r = self._session.get(uri, headers=headers)
        if r.status_code != 200:
            print(r.content)
            raise Exception("Failed to open!")
        soup = BeautifulSoup(r.content, 'static.parser')
        table = soup.find_all("tbody")[0]
        res = "Фамилия,Имя Отчество,\"Оценка/100,00\"\n"
        for cell in table.contents:
            # print(cell.get("class", 0))
            if cell.get("class", [0])[0] in ["emptyrow", 0]:
                break
            # print(cell.contents[2])
            person = cell.contents[2].contents[0].contents[0]
            # print(person)
            # print(cell.contents[2].contents[0])
            res += person.split()[0] + "," + " ".join(person.split()[1:]) + ",givenin\n"
        with open(self._name_template.format(task_id), 'w') as f:
            f.write(res)
        return self._name_template.format(task_id)

# if __name__ == "__main__":
#     CourseUpdFetcher("token.json", [], "")._fetch_contest_results(18983)
