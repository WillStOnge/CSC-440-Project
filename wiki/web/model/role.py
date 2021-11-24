class Role:
    def __init__(self, role_id: int, role_name: str):
        self._role_id = role_id
        self._role_name = role_name

    def __eq__(self, other):
        if isinstance(other, Role):
            return (self._role_id == other._role_id) and (self._role_name == other._role_name)
        else:
            return False

    def __hash__(self):
        return hash((self._role_id, self._role_name))

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
