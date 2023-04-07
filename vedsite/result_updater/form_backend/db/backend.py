from .db import DBEngine


class DBBackend:
    def __init__(self, db_name, db_login, db_password):
        self._engine = DBEngine(db_name, db_login, db_password)

    # MARK: disciplines

    def get_disciplines(self):
        raise NotImplementedError

    def create_discipline(self):
        raise NotImplementedError

    # MARK: tasks

    def get_tasks(self, discipline_id):
        raise NotImplementedError

    def add_task(self):
        raise NotImplementedError

    def set_check_system_credentials(self):
        raise NotImplementedError

    def get_credentials(self, discipline_id):
        raise NotImplementedError

    # ...
