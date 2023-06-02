import requests as req
import json
import webbrowser
from flask import Flask, request
from bs4 import BeautifulSoup
from ..protocol import Authorizer
import lxml
# import .constants as const
# try:
from .constants import *
# except:
#     from constants import *


class YaContestAuthorizer(Authorizer):
    def init(self, authorize=False):
        Authorizer.init(self)
        self._session = None
        if authorize:
            self.authorize({"login": AUTH_LOGIN,
                            "password": AUTH_PASSWD})

    def authorize(self, credentials):

        session = req.Session()

        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36",
                   }
        uri0 = "https://passport.yandex.ru/auth"
        r = session.get(uri0, headers=headers)

        soup = BeautifulSoup(r.text, "lxml")
        csrf_token = soup.find("input", {"name": "csrf_token"}).get("value")
        sub = r.text[r.text.find("process_uuid="):]
        process_uuid = sub[:sub.find("\"")].split("=")[1]

        uri1 = "https://passport.yandex.ru/registration-validations/auth/multi_step/start"
        post_data = {"csrf_token": csrf_token,
                     "login": credentials["login"],
                     "process_uuid": process_uuid,
                     }
        r = session.post(uri1,
                         data=post_data,
                         headers=headers)
        login_post_res = json.loads(r.text)

        uri2 = "https://passport.yandex.ru/registration-validations/auth/multi_step/commit_password"
        post_data = {"csrf_token": csrf_token,
                     "track_id": login_post_res["track_id"],
                     "password": credentials["password"],
                     }
        r = session.post(uri2, data=post_data, headers=headers)

        # auth_cookie = [cookie.split(";")[0] for cookie in r.headers["Set-Cookie"].split(",")[::2]]
        # auth_cookie = ", ".join(auth_cookie)
        self._session = session

    def get_session(self):
        if self._session is None:
            raise Exception("Perform auth first!")
        return self._session

    def update_authorization(self):
        # uri = "https://passport.yandex.ru/auth/update"
        # headers = {"Cookie": COOKIE}
        # r = req.get(uri, headers=headers)
        # if r.status_code == 200 and json.loads(r.content)["status"] == "ok":
        #     return True
        # # if cookie update failed
        # return self._get_auth_cookies()
        self.authorize({"email": AUTH_LOGIN,
                        "password": AUTH_PASSWD})
        return self.get_token()

    def logout(self):
        req = self._session.get("https://passport.yandex.ru/passport?mode=embeddedauth&action=logout")
        print(req.history)
        print(req.status_code)

    # def _get_auth_cookies(self):
    #     raise Exception("Replace cookies!")
    # def logout(self):
    #


if __name__ == "__main__":
    Authorizer()  # .authorize({"login": AUTH_LOGIN,
    #  "password": AUTH_PASSWD}
    # )
