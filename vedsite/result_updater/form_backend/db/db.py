
class DBEngine:
    def __init__(self, db_name, db_login, db_password):
        self._login("localhost", db_name, db_login, db_password)

    def _login(self, host, db_name, login, password):
        raise NotImplementedError

    def select_rows(self, ):
        """
        args: TODO: discuss
        :return: target query rows
        """
        raise NotImplementedError

    def add_row(self, table_name, row):
        """
        :param table_name: name of the table to add row to (string)
        :param row: dictionary. Keys are columns, values are corresponding values of the row.
        :return:
        """
        raise NotImplementedError
