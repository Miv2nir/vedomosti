from ...form_backend.google_sheets.backend import GSheetsBackend


class LoginFormResponseReader:
    def __init__(self, form_engine: GSheetsBackend, sheet_columns: list):
        self._engine = form_engine
        self._columns = sheet_columns

    def get_new_responses(self, bound_date):
        pass
