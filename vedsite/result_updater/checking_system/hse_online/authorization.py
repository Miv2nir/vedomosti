import requests as req
import json
import webbrowser
from flask import Flask, request
from .constants import *
from ..protocol import Authorizer


class HSEOnlineAuthorizer(Authorizer):
    _token = None

    def __init__(self, authorize=True):
        Authorizer.__init__(self, authorize)
        self._session = None
        if authorize:
            self.authorize({"login": AUTH_LOGIN,
                             "password": AUTH_PASSWD})

    def authorize(self, credentials):

        session = req.Session()

        uri1 = "https://auth.hse.ru/adfs/oauth2/authorize/?response_mode=form_post&" \
               "state={{\"system_id\":29," \
                    "\"redirect_url\":\"https://online.hse.ru/login/index.php\"}}&" \
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
        r = session.post(uri1, headers=post_headers, data=post_data)

        form_code = str(r.content)
        code_substr = "<input type=\"hidden\" name=\"code\" value=\""
        st_pos = form_code.find(code_substr) + len(code_substr)
        form_code = form_code[st_pos:]
        code = form_code[:form_code.find("\"")]

        uri2 = "https://lk.hse.ru:443/api/sso/adfs-side-auth"
        post_data = {"code": code,
                     "state": "{\"system_id\":29,\"redirect_url\":\"https://online.hse.ru/login/index.php\"}"
                     }
        r = session.post(uri2,
                     data=post_data,
                     )
        self._session = session

        # auth_cookie = r.history[-2].headers["Set-Cookie"].split(";")[0]
        # self._token = auth_cookie

    def get_session(self):
        if self._session is None:
            raise Exception("Perform auth first!")
        return self._session

    def update_authorization(self):
        self.authorize({"login": AUTH_LOGIN,
                        "password": AUTH_PASSWD})
        return self.get_session()


if __name__ == "__main__":
    authzr = Authorizer()
    t = authzr.get_token()
    print(t)