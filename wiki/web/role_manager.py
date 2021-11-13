from wiki.web.role import Role

class RoleManager:
    """
    Class used to manage roles in the database.
    """
    def __init__(self, database):
        self._database = database


    def create_role(self, role: Role) -> bool:
        pass


    def read_role(self, role_name: str) -> Role:
        pass


    def delete_role(self, role: Role) -> bool:
        pass


    def read_roles(self, role_name: str) -> list:
        pass


    def add_role_to_user(self, user: User, role: Role) -> bool:
        pass


    def remove_role_to_user(self, user: User, role: Role) -> bool:
        pass