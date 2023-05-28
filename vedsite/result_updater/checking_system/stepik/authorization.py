import requests as req
import json
import webbrowser
from flask import Flask, request
from bs4 import BeautifulSoup
from ..protocol import Authorizer
from .constants import *


class StepikAuthorizer(Authorizer):
    def __init__(self, authorize=True):
        Authorizer.__init__(self)
        self._session = None
        # if authorize:
        #    self.authorize({"email": AUTH_LOGIN,
        #                    "password": AUTH_PASSWD})

    def authorize(self, credentials):

        session = req.session()

        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36"}
        uri1 = "https://stepik.org/api/users/login"

        r = session.get(uri1, headers=headers)

        soup = BeautifulSoup(r.text, "lxml")
        # csrf_token = soup.find("meta", {"name": "csrftoken"})["content"]

        post_data = {"email": credentials["login"],
                     "password": credentials["password"],
                     }
        r = session.post(uri1, data=post_data, headers=headers)
        self._session = session

    def get_session(self):
        if self._session is None:
            raise Exception("Perform auth first!")
        return self._session

    def update_authorization(self):
        self.authorize({"login": AUTH_LOGIN,
                        "password": AUTH_PASSWD})
        return self.get_session()

    # def logout(self):
        # найти url для logout
        # req.get(...)
