import os, binascii, hashlib
from functools import wraps
from flask import current_app
from flask_login import current_user
from wiki.web.user_manager import UserManager
from wiki.web.database import Database


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


def make_salted_hash(password, salt=None):
    if not salt:
        salt = os.urandom(64)
    d = hashlib.sha512()
    d.update(salt[:32])
    d.update(password)
    d.update(salt[32:])
    return binascii.hexlify(salt) + d.hexdigest()


def check_hashed_password(password, salted_hash):
    salt = binascii.unhexlify(salted_hash[:128])
    return make_salted_hash(password, salt) == salted_hash


def protect(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_app.config.get('PRIVATE') and not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        return f(*args, **kwargs)
    return wrapper
