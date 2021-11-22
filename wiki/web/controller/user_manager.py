from wiki.web.model import User
from wiki.web.util import Database

class UserManager:
    """
    Class used to manage users in the database.
    """
    def __init__(self, database: Database):
        self._database = database


    def create(self, user_name: str, password: str, is_active: bool) -> User:
        """
        Inserts a new user into the database.

        :param user_name: Name of the user to be created.
        :param password: Raw password of the user to be created.
        :param is_active: Flag whether the user is active or not.

        :returns: The newly created user or None if the user could not be created.
        """
        # Check if user already exists.
        select_query = "SELECT user_id FROM user WHERE user_name = {};".format(user_name)
        print(select_query)
        if self._database.execute_query_for_result(select_query) is not None:
            return None

        # Insert the user.
        insert_query = "INSERT INTO user (user_name, password, is_active) VALUES ({}, {}, {});".format(user_name, password, is_active)
        print(insert_query)
        if not self._database.execute_query(insert_query):
            return None

        # Return instance of new user.
        return self.read(user_name)


    def read(self, user_name: str) -> User:
        """
        Reads user's data from the database an returns it.
        
        :param user_name: Username of the user to be retrieved from the database.

        :returns: An instance of the User from the database. Returns None if the user is not found.
        """
        query = "SELECT user_id, user_name, password, is_active FROM user WHERE user_name = '{}';".format(user_name)
        result = self._database.execute_query_for_result(query)

        if result != None:
            return User(result[0]["user_id"], user_name, str(result[0]["password"]), result[0]["is_active"])
        else:
            return None


    def read_all(self) -> list:
        """
        Reads all user's data from the database an returns it.

        :returns: An instance of all of the users from the database. Returns None if no roles exist.
        """
        query = "SELECT user_id, user_name, password, is_active FROM user;"
        result = self._database.execute_query_for_result(query)

        if result != None:
            return [User(user["user_id"], user["user_name"], user["password"], user["is_active"]) for user in result]
        else:
            return None


    def update(self, user: User) -> bool:
        """
        Updates a user in the database.

        :param user: Instance of the User which should be updated.

        :returns: True if the update was successful and false otherwise.
        """
        query = "UPDATE user \
                SET user_name = {}, password = {}, is_active = {} \
                WHERE user_id = {}".format(user.user_name, user.password, user.is_active, user.user_id)
        return self._database.execute_query(query)
        

    def delete(self, user: User) -> bool:
        """
        Deletes a user from the database.

        :param user: Instance of the User which should be deleted.

        :returns: True if the deletion was successful and false otherwise.
        """
        return self._database.execute_query("DELETE user WHERE user_id = {}".format(user.user_id))