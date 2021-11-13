from wiki.web.controller.user_manager import UserManager
from wiki.web.util.database import Database

class User:
    def __init__(self, user_id, user_name, password, is_active):
        self._user_id = user_id
        self._user_name = user_name
        self._password = password
        self._is_active = is_active


    def save(self):
        self.get_manager().update(self.name, self.data)


    def is_authenticated(self):
        return self.data.get('authenticated')


    def is_active(self):
        return self.data.get('active')


    def is_anonymous(self):
        return False


    def get_id(self):
        return self.name


    def check_password(self, password):
        return check_hashed_password(password, self.get('hash'))


    def get_manager() -> UserManager:
        return UserManager(Database())


    @property
    def user_id(self):
        return self._user_id

        
    @property
    def user_name(self):
        return self._user_name

        
    @property
    def password(self):
        return self._password

        
    @property
    def is_active(self):
        return self._is_active


    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id


    @user_name.setter
    def user_name(self, user_name):
        self._user_name = user_name


    @password.setter
    def password(self, password):
        self._password = password


    @is_active.setter
    def is_active(self, is_active):
        self._is_active = is_active