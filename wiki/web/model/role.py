from wiki.web.user import User
from wiki.web.controller.role_manager import RoleManager
from wiki.web.util.database import Database

class Role:
    def __init__(self, role_id: int, role_name: str):
        self._role_id = role_id
        self._role_name = role_name


    def get_manager() -> RoleManager:
        return RoleManager(Database())


    @property
    def role_id(self):
        return self._role_id


    @property
    def role_name(self):
        return self._role_name


    @role_name.setter
    def role_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Incompatible type, excepted string got ', type(value))
        self._role_name = value