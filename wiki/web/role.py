from wiki.web.user import User
from wiki.web.role_manager import RoleManager
from wiki.web.database import Database

class Role:
    _name: str

    def __init__(self, role_name: str):
        _name = role_name

    @property
    def name(self):
        return _name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Incompatible type, excepted string got ', type(value))
        _name = value


    def get_manager() -> RoleManager:
        return RoleManager(Database())