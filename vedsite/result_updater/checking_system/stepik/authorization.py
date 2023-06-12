import requests as req
import json
import webbrowser
from flask import Flask, request
from bs4 import BeautifulSoup
from ..protocol import Authorizer
from .constants import *


class InvalidCredentialsException(Exception):
    "Invalid Stepik Credentials"
    pass


class StepikAuthorizer(Authorizer):
    def init(self, authorize=True):
        Authorizer.init(self)
        self._session = None
        self._token = None
        if authorize:
            self.authorize({"client_id": AUTH_LOGIN,
                            "client_secret": AUTH_PASSWD})

    def authorize(self, credentials):

        auth = req.auth.HTTPBasicAuth(credentials["client_id"], credentials["client_secret"])
        response = req.post('https://stepik.org/oauth2/token/',
                            data={'grant_type': 'client_credentials'},
                            auth=auth)
        token = response.json().get('access_token', None)
        if not token:
            print('Unable to authorize with provided credentials')
            raise InvalidCredentialsException("Invalid Stepik Credentials")
        self._token = token

    def get_token(self):
        if self._token is None:
            raise Exception("Perform auth first!")
        return self._token

    def update_authorization(self):
        self.authorize({"client_id": AUTH_LOGIN,
                        "client_secret": AUTH_PASSWD})
        return self.get_token()
