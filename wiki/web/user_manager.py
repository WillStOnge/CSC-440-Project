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

        :returns: The newly created user or None if the user could not be created.
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
        select_query = "SELECT user_id FROM user WHERE user_name = {};".format(user_name)
        result = self._database.execute_query_for_result(select_query)

        print(result)

        if len(result) > 0:
            return User(1, user_name, password, is_active)
        else:
            return None


    def get_user(self, user_id: int) -> User:
        """
        Reads user's data from the database an returns it.
        
        :param user_id: Id of the user to be retrieved from the database.
        """
        pass


    def delete_user(self, user: User) -> bool:
        """
        Deletes a user from the database.

        :param user: Instance of the User which should be deleted.

        :returns: True if the deletion was successful and false otherwise.
        """
        try:
            self._database.execute_query("DELETE user WHERE user_id = ?", user.user_id)
            return True
        except:
            return False


    def update(self, user: User):
        """
        Updates a user into the database.

        :param user: Instance of the User which should be updated.
        """
        pass