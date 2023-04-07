from ..__protocol import FormBackendProtocol


class GSheetsBackend(FormBackendProtocol):
    def __init__(self, sheets_engine):
        super().__init__(sheets_engine)

    def open(self, path):
        try:
            self._form = self.engine.open(path)
        except Exception as e:
            self.create(path)
        self._sheet = None

    def save(self):
        pass

    def create(self, path):
        self._form = self.engine.create(path)

    def select_sheet(self, sheet_name):
        self._sheet = self._form.worksheet(sheet_name)

    def get_cell_value(self, cell_addr):
        return self._sheet.acell(cell_addr).value

    def set_cell_value(self, cell_addr, value):
        self._sheet.update_acell(cell_addr, value)

    def insert_row(self, ind):
        self._sheet.insert_row([None], ind)
