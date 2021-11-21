from wiki.web.model import Role, User
from wiki.web.util import Database

class RoleManager:
    """
    Class used to manage roles in the database.
    """
    def __init__(self, database: Database):
        self._database = database


    def create(self, role_name: str) -> Role:
        """
        Inserts a new role into the database.

        :param role_name: Name of the role to be created.

        :returns: The newly created role or None if the role could not be created.
        """
        # Check if role already exists.
        select_query = "SELECT role_id FROM role WHERE role_name = {};".format(role_name)
        if len(self._database.execute_query_for_result(select_query)) > 0:
            return None

        # Insert the role.
        insert_query = "INSERT INTO role (role_name) VALUES ({});".format(role_name)
        if not self._database.execute_query(insert_query):
            return None

        # Return instance of new role.
        return self.read(role_name)


    def read(self, role_name: str) -> Role:
        """
        Reads role's data from the database an returns it.
        
        :param role_name: Name of the role to be retrieved from the database.

        :returns: An instance of the Role from the database. Returns None if the role is not found.
        """
        query = "SELECT role_id, role_name FROM role WHERE role_name = {};".format(role_name)
        result = self._database.execute_query_for_result(query)

        if result != None:
            return Role(result[0]["role_id"], role_name)
        else:
            return None


    def read_all(self) -> list:
        """
        Reads all role's data from the database an returns it.

        :returns: An instance of all of the roles from the database. Returns None if no roles exist.
        """
        query = "SELECT role_id, role_name FROM role;"
        result = self._database.execute_query_for_result(query)

        if result != None > 0:
            return [Role(role["role_id"], role["role_name"]) for role in result]
        else:
            return None


    def update(self, role: Role) -> bool:
        """
        Updates a role in the database.

        :param role: Instance of the Role which should be updated.

        :returns: True if the update was successful and false otherwise.
        """
        query = "UPDATE role \
                SET role_name = {} \
                WHERE role_id = {}".format(role.role_name, role.role_id)
        return self._database.execute_query(query)


    def delete(self, role: Role) -> bool:
        """
        Deletes a role from the database.

        :param role: Instance of the Role which should be deleted.

        :returns: True if the deletion was successful and false otherwise.
        """
        return self._database.execute_query("DELETE role WHERE role_id = {}".format(role.role_id))


class RoleAssignmentManager:
    """
    Class used to manage role assignments in the database.
    """
    def __init__(self, database):
        self._database = database


    def assign_role_to_user(self, user: User, role: Role) -> bool:
        """
        Assigns a role from a user.
        
        :param user: User to assign the role to.
        :param role: Role to be assigned.

        :returns: True if the assignment was successful and false otherwise.
        """
        # Make sure the role and user exist in the database.
        select_role_query = "SELECT role_id FROM role WHERE role_id = {};".format(role.role_id)
        select_user_query = "SELECT user_id FROM user WHERE user_id = {};".format(user.user_id)

        if len(self._database.execute_query_for_result(select_role_query)) == 0:
            return False
        if len(self._database.execute_query_for_result(select_user_query)) == 0:
            return False

        # Check if role assignment already exists.
        select_query = "SELECT role_id FROM role_assignemnt WHERE role_id = {} AND user_id = {};".format(role.role_id, user.user_id)

        if len(self._database.execute_query_for_result(select_query)) > 0:
            return False

        # Insert the role assignemnt.
        insert_query = "INSERT INTO role_assignment (user_id, role_id) VALUES ({}, {});".format(user.user_id, role.role_id)
        return self._database.execute_query(insert_query)


    def unassign_role_to_user(self, user: User, role: Role) -> bool:
        """
        Unassigns a role from a user.
        
        :param user: User to unassign the role from.
        :param role: Role to be unassigned.

        :returns: True if the unassignment was successful and false otherwise.
        """
        return self._database.execute_query("DELETE role_assignment WHERE role_id = {} AND user_id = {}".format(role.role_id, user.user_id))


    def get_user_roles(self, user: User) -> list:
        """
        Reads the user's role data from the database and returns it.
        
        :param user: User to get roles for.

        :returns: List of roles assigned to a user. Returns None if no roles are assigned.
        """
        query = "SELECT role.role_id AS role_id, role_name FROM role INNER JOIN role_assignment \
                ON role_assignment.role_id = role.role_id WHERE user_id = {};".format(user.user_id)
        result = self._database.execute_query_for_result(query)

        if result != None > 0:
            return [Role(role["role_id"], role["role_name"]) for role in result]
        else:
            return None