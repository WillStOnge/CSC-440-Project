"""
    User classes & helpers
    ~~~~~~~~~~~~~~~~~~~~~~
"""

class RoleManager:
    def __init__(self):
        pass

    def create_role(self, role: Role) -> bool:
        pass

    def read_role(self, role_name: str) -> Role:
        pass

    def update_role(self, role: Role) -> bool:
        pass

    def delete_role(self, role: Role) -> bool:
        pass

    def read_roles(self, role_name: string) -> List[Role]:
        pass

    def add_role_to_user(self, user: User, role: Role) -> bool:
        pass

    def remove_role_to_user(self, user: User, role: Role) -> bool:
        pass


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