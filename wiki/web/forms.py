"""
    Forms
    ~~~~~
"""
from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import TextField
from wtforms import TextAreaField
from wtforms import PasswordField
from wtforms.validators import InputRequired
from wtforms.validators import ValidationError

from wiki.core import clean_url
from wiki.web import current_wiki
from wiki.web import current_users


class URLForm(FlaskForm):
    url = TextField('', [InputRequired()])

    def validate_url(form, field):
        if current_wiki.exists(field.data):
            raise ValidationError('The URL "%s" exists already.' % field.data)

    def clean_url(self, url):
        return clean_url(url)


class SearchForm(FlaskForm):
    term = TextField('', [InputRequired()])
    ignore_case = BooleanField(
        description='Ignore Case',
        # FIXME: default is not correctly populated
        default=True)


class EditorForm(FlaskForm):
    title = TextField('', [InputRequired()])
    body = TextAreaField('', [InputRequired()])
    tags = TextField('')


class LoginForm(FlaskForm):
    name = TextField('', [InputRequired()])
    password = PasswordField('', [InputRequired()])

    def validate_name(form, field):
        user = current_users.read_name(field.data)
        if user == None:
            raise ValidationError('This username does not exist.')

    def validate_password(form, field):
        user = current_users.read_name(form.name.data)
        if user == None:
            raise ValidationError('This username does not exist.')
        if not user.check_password(field.data):
            raise ValidationError('Username and password do not match.')


class UserForm(FlaskForm):
    name = TextField('', [InputRequired()])
    password = PasswordField('', [InputRequired()])


class RoleForm(FlaskForm):
    name = TextField('', [InputRequired()])
