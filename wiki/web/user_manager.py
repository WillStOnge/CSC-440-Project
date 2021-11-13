from wiki.web.role import User

class UserManager:
    """
    Class used to manage users in the database.
    """
    def __init__(self, database: Database):
        self._database = database


    def add_user(self, user_name: str, password: str, is_active: bool) -> User:
        """
        Inserts a new user into the database.

        :param user_name: Name of the user to be created.
        :param password: Raw password of the user to be created.
        :param is_active: Flag whether the user is active or not.

        :returns: The newly created user or None if the user could not be created.As a reminder, HW3 is due 
        """
        # Check if user already exists.
        select_query = "SELECT user_id FROM user WHERE user_name = {};".format(user_name)
        if len(self._database.execute_query_for_result(select_query)) > 0:
            return None

        # Insert the user.
        insert_query = "INSERT INTO user (user_name, password, is_active) VALUES ({}, {}, {});".format(user_name, password, is_active)
        if not self._database.execute_query(insert_query):
            return None

        # Return instance of new user.
        return self.get_user(user_name)


    def get_user(self, user_name: int) -> User:
        """
        Reads user's data from the database an returns it.
        
        :param user_name: Username of the user to be retrieved from the database.

        :returns: An instance of the User from the database. Returns None if the user is not found.
        """
        query = "SELECT user_id, user_name, password, is_active FROM user WHERE user_name = {};".format(user_name)
        result = self._database.execute_query_for_result(query)

        if len(result) > 0:
            return User(result[0]["user_id"], user_name, result[0]["password"], result[0]["is_active"])
        else:
            return None


    def delete_user(self, user: User) -> bool:
        """
        Deletes a user from the database.

        :param user: Instance of the User which should be deleted.

        :returns: True if the deletion was successful and false otherwise.
        """
        return self._database.execute_query("DELETE user WHERE user_id = {}".format(user.user_id))
        

    def update(self, user: User) -> bool:
        """
        Updates a user into the database.

        :param user: Instance of the User which should be updated.

        :returns: True if the update was successful and false otherwise.
        """
        query = "UPDATE user \
                SET user_name = {}, password = {}, is_active = {} \
                WHERE user_id = {}".format(user.user_name, user.password, user.is_active, user.user_id)
        return self._database.execute_query(query)