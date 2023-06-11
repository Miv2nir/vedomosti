# coding=utf-8
import requests as req
import json
import webbrowser
from flask import Flask, request
from .constants import *


class Authorizer:
    _token = None

    def __init__(self):
        self._token = None
        # self._authorize({"email": AUTH_LOGIN,
                         # "password": AUTH_PASSWD})

    def authorize(self, credentials):
        uri1 = "https://auth.hse.ru/adfs/oauth2/authorize/?response_mode=form_post&" \
               "state={{\"system_id\":19," \
                    "\"redirect_url\":\"https://lms.hse.ru/elk_auth.php\"}}&" \
               "redirect_uri=https://lk.hse.ru/api/sso/adfs-side-auth&" \
               "client_id={}&response_type=code".format(AUTH_CLIENT_ID)
        post_data = {"UserName": credentials["login"],
                     "Kmsi": True,
                     "AuthMethod": "FormsAuthentication",
                     "Password": credentials["password"]}
        post_headers = {"Accept": "text/static,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/"
                                  "apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "ru-RU,ru;q=0.9",
                        "Connection": "keep-alive",
                        "Content-Type": "application/x-www-form-urlencoded"}
        r = req.post(uri1, headers=post_headers, data=post_data)

        form_code = str(r.content)
        code_substr = "<input type=\"hidden\" name=\"code\" value=\""
        st_pos = form_code.find(code_substr) + len(code_substr)
        form_code = form_code[st_pos:]
        code = form_code[:form_code.find("\"")]

        uri2 = "https://lk.hse.ru/api/sso/adfs-side-auth"
        post_data = {"code": code,
                     "state": "{\"system_id\":19,\"redirect_url\":\"https://lms.hse.ru/elk_auth.php\"}"
                     }
        r = req.post(uri2,
                     data=post_data
                     )
        auth_cookie = [cookie.split(";")[0] for cookie in r.headers["Set-Cookie"].split(", ")
                       if cookie.split(";")[0] != cookie]
        auth_cookie = "; ".join(auth_cookie)

        self._token = auth_cookie

    def get_token(self):
        if self._token is None:
            raise Exception("Perform auth first!")
        return self._token

    def update_authorization(self):
        self.authorize({"login": AUTH_LOGIN,
                        "password": AUTH_PASSWD})
        return self.get_token()

    def logout(self):
        req.get("https://lms.hse.ru/index.php?logout=true",
                headers={"Cookie": self.get_token()}
                )


if __name__ == "__main__":
    authzr = Authorizer()
    t = authzr.get_token()
    r = req.get("https://lms.hse.ru/professor.php?lessons_ID=134473", headers={"Cookie": t})
    print("Методы оптимизации" in r.text)

    authzr.logout()
    r = req.get("https://lms.hse.ru/professor.php?lessons_ID=134473", headers={"Cookie": t})
    print("Методы оптимизации" in r.text)
