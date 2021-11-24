"""
    Routes
    ~~~~~~
"""
from flask import Blueprint, current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from wiki.core import Processor
from wiki.web.controller import RoleAssignmentManager, RoleManager
from wiki.web.forms import EditorForm, UserForm
from wiki.web.forms import LoginForm
from wiki.web.forms import SearchForm
from wiki.web.forms import URLForm
from wiki.web import current_wiki, Database
from wiki.web import current_users
from wiki.web.util import protect

bp = Blueprint('wiki', __name__)
current_user = current_user


@bp.route('/')
@protect
def home():
    page = current_wiki.get('home')
    role_assignment_manager = RoleAssignmentManager(Database())
    user_roles = role_assignment_manager.get_user_roles(current_user)
    user_admin_role = next((role_object for role_object in user_roles if role_object.role_name == "admin"), None)
    if user_admin_role is not None:
        current_user.is_admin = True
    if page:
        return display('home')
    return render_template('home.html')


@bp.route('/index/')
@protect
def index():
    pages = current_wiki.index()
    return render_template('index.html', pages=pages)


@bp.route('/<path:url>/')
@protect
def display(url):
    page = current_wiki.get_or_404(url)
    return render_template('page.html', page=page)


@bp.route('/create/', methods=['GET', 'POST'])
@protect
def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for('wiki.edit', url=form.clean_url(form.url.data)))
    return render_template('create.html', form=form)


@bp.route('/edit/<path:url>/', methods=['GET', 'POST'])
@protect
def edit(url):
    page = current_wiki.get(url)
    form = EditorForm(obj=page)
    if form.validate_on_submit():
        if not page:
            page = current_wiki.get_bare(url)
        form.populate_obj(page)
        page.save()
        flash('"%s" was saved.' % page.title, 'success')
        return redirect(url_for('wiki.display', url=url))
    return render_template('editor.html', form=form, page=page)


@bp.route('/preview/', methods=['POST'])
@protect
def preview():
    data = {}
    processor = Processor(request.form['body'])
    data['html'], data['body'], data['meta'] = processor.process()
    return data['html']


@bp.route('/move/<path:url>/', methods=['GET', 'POST'])
@protect
def move(url):
    page = current_wiki.get_or_404(url)
    form = URLForm(obj=page)
    if form.validate_on_submit():
        newurl = form.url.data
        current_wiki.move(url, newurl)
        return redirect(url_for('wiki.display', url=newurl))
    return render_template('move.html', form=form, page=page)


@bp.route('/delete/<path:url>/')
@protect
def delete(url):
    page = current_wiki.get_or_404(url)
    current_wiki.delete(url)
    flash('Page "%s" was deleted.' % page.title, 'success')
    return redirect(url_for('wiki.home'))


@bp.route('/tags/')
@protect
def tags():
    tags = current_wiki.get_tags()
    return render_template('tags.html', tags=tags)


@bp.route('/tag/<string:name>/')
@protect
def tag(name):
    tagged = current_wiki.index_by_tag(name)
    return render_template('tag.html', pages=tagged, tag=name)


@bp.route('/search/', methods=['GET', 'POST'])
@protect
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = current_wiki.search(form.term.data, form.ignore_case.data)
        return render_template('search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('search.html', form=form, search=None)


@bp.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = current_users.read_name(form.name.data)
        login_user(user)
        user.set_authenticated(True)
        flash('Login successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.index'))
    return render_template('login.html', form=form)


@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set_authenticated(False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.index'))


@bp.route('/user/')
@protect
def user_index():
    users = current_users.read_all()
    return render_template('users.html', users=users)


@bp.route('/user/create/', methods=['POST', 'GET'])
@protect
def user_create():
    form = UserForm()
    if form.validate_on_submit():
        new_user = current_users.create(form.name.data, form.password.data, 1)
        if new_user is None:
            return redirect("/user/{}/".format(form.name.data))
        else:
            return redirect("/user/{}/".format(new_user.user_name))
    return render_template('create_user.html', form=form)


@bp.route('/user/<string:user_name>/')
@protect
def user_admin(user_name):
    user = current_users.read_name(user_name)
    user_roles = RoleAssignmentManager(Database()).get_user_roles(user)
    return render_template('user.html', user=user, user_roles=user_roles)


@bp.route('/user/delete/<int:user_id>/')
@protect
def user_delete(user_id):
    deleted_user = current_users.read_id(user_id)
    deleted = current_users.delete(deleted_user)

    if deleted is not None:
        return redirect(url_for('wiki.user_index'))
    return 'Could not delete user'


@bp.route('/roles')
@protect
def roles():
    role_manager = RoleManager(Database())
    all_roles = role_manager.read_all()
    temp_user = current_user
    temp_user_roles = RoleAssignmentManager(Database()).get_user_roles(temp_user)
    return render_template('roles.html', roles=all_roles)


# TODO : unit test
@bp.route('/role/<int:user_id>/')
def role_list_assigned(user_id):
    role_assignment_manager = RoleAssignmentManager(Database())
    user = current_users.read_id(user_id)
    user_roles = role_assignment_manager.get_user_roles(user)
    if user_roles is not None:
        return user_roles
    return 'Could not return role assigned to user'


# TODO: unit test
@bp.route('/roles/create/<string:role_name>')
def role_create(role_name):
    role_manager = RoleManager(Database())
    user_role = role_manager.create(role_name)
    if user_role is not None:
        return user_role
    return 'Could not create role: ' + role_name


# TODO: unit test
@bp.route('/roles/delete/<string:role_name>/')
def role_delete(role_name):
    role_manager = RoleManager(Database())
    role_to_be_deleted = role_manager.read(role_name)
    deleted_role = role_manager.delete(role_to_be_deleted)
    if deleted_role is not None:
        return deleted_role
    return 'Could not delete role: ' + role_name


# TODO: unit test
@bp.route('/role/assign/<int:user_id>/<string:role_name>/')
def role_assign(user_id, role_name):
    role_manager = RoleManager(Database())
    role = role_manager.read(role_name)
    if role is None:
        return 'Could not find role: "%s" ' % role_name

    role_assignment_manager = RoleAssignmentManager(Database())
    user = current_users.read_id(user_id)
    user_roles = role_assignment_manager.get_user_roles(user)

    # Given a role name, checks if user has a role with that role name
    # returns None if role is not found
    existing_user_role = next((role_object for role_object in user_roles if role_object.role_name == role_name), None)

    if existing_user_role is not None:
        flash('User "%s" already has role: "%s"' % (user.user_name, role.role_name), 'warning')
        return redirect(url_for('wiki.user_admin', user_name=user.user_name))

    assigned_role = role_assignment_manager.assign_role_to_user(user, role)
    if assigned_role is not None:
        flash('Role "%s" was assigned to user "%s"' % (role.role_name, user.user_name), 'success')
        return redirect(url_for('wiki.user_admin', user_name=user.user_name))
    return 'Could not assign role: "%s" to user id: "%s"' % (role_name, user_id)


# TODO: unit test
@bp.route('/role/unassign/<int:user_id>/<string:role_name>/')
def role_unassign(user_id, role_name):
    role_assignment_manager = RoleAssignmentManager(Database())
    user = current_users.read_id(user_id)
    roles = role_assignment_manager.get_user_roles(user)

    # Given a role name, checks if user has a role with that role name
    # returns None if role is not found
    role = next((role_object for role_object in roles if role_object.role_name == role_name), None)

    if role is not None:
        role_unassigned = role_assignment_manager.unassign_role_to_user(user, role)
        if role_unassigned:
            flash('Role "%s" was unassigned from user "%s"' % (role.role_name, user.user_name), 'success')
            return redirect(url_for('wiki.user_admin', user_name=user.user_name))
    return 'Could not unassign role'


"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
