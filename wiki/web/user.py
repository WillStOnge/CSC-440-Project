import os, binascii, hashlib
from functools import wraps
from flask import current_app
from flask_login import current_user


class UserManager(object):
    """
    A very simple user Manager, that saves it's data to a database.
    """
    def __init__(self, conn):
        self.conn = conn


    def add_user(self, user):
        """
        Inserts a new user into the database.
        """
        # Check if user already exists.
        # Insert the user.
        # Return instance of new user.
        pass


    def get_user(self, name):
        """
        Reads user's data from the database an returns it.
        """
        pass


    def delete_user(self, name):
        """
        Deletes a user into the database.
        """
        users = self.read()
        if not users.pop(name, False):
            return False
        self.write(users)
        return True


    def update(self, name, userdata):
        """
        Updates a user into the database.
        """
        data = self.read()
        data[name] = userdata
        self.write(data)


class User(object):
    def __init__(self, manager, name, data):
        self.manager = manager
        self.name = name
        self.data = data


    def get(self, option):
        return self.data.get(option)


    def set(self, option, value):
        self.data[option] = value
        self.save()


    def save(self):
        self.manager.update(self.name, self.data)


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
