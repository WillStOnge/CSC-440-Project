from wiki.web.util import check_hashed_password, make_salted_hash


class User:
    def __init__(self, user_id, user_name, password, is_active):
        self._user_id = user_id
        self._user_name = user_name
        self._password = password
        self._is_active = is_active
        self._is_authenticated = False
        self._is_admin = False

    def save(self):
        self.get_manager().update(self.name, self.data)

    def is_authenticated(self):
        return self._is_authenticated

    def set_authenticated(self, is_authenticated):
        self._is_authenticated = is_authenticated

    def is_active(self):
        return self.data.get('active')

    def is_anonymous(self):
        return False

    def get_id(self):
        return self._user_name

    def check_password(self, password):
        return check_hashed_password(password, self.password)

    @property
    def is_admin(self):
        return self._is_admin

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

    @is_admin.setter
    def is_admin(self, is_admin):
        self._is_admin = is_admin

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
