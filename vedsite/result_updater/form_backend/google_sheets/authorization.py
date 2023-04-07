import os.path
from googleapiclient.discovery import build
# from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import gspread as gc

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']


class Authorizer:
    def __init__(self):
        self._authorize()

    def _authorize(self):
        self._creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        token_path = "/".join(__file__.split("/")[:-1]) + "/_token.json"
        if os.path.exists(token_path):
            self._creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self._creds or not self._creds.valid:
            if self._creds and self._creds.expired and self._creds.refresh_token:
                self._creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("/".join(__file__.split("/")[:-1]) + "/" + '_credentials.json', SCOPES)
                self._creds = flow.run_local_server(port=64272)
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(self._creds.to_json())

        # credentials = Credentials.from_service_account_file("_credentials.json", scopes=SCOPES)
        # self.engine = service = build('sheets', 'v4', credentials=self._creds)
        self.engine = gc.authorize(self._creds)  # build('sheets', 'v4', credentials=self._creds)


if __name__ == "__main__":
    Authorizer()