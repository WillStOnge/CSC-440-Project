from flask import Blueprint, flash, redirect, render_template, request, url_for, session, jsonify, current_app
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import secure_filename
from functools import wraps
import os

import config
from wiki.web.forms import EditorForm, UserForm, RoleForm, LoginForm, SearchForm, URLForm
from wiki.web.controller import RoleAssignmentManager, RoleManager
from wiki.web import current_wiki, current_users, Database
from wiki.web.util import protect
from wiki.core import Processor


bp = Blueprint('wiki', __name__)


def requires_access_level(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('wiki.login'))
            current_user_roles = RoleAssignmentManager(Database()).get_user_roles(current_user)
            matching_role = next((role_object for role_object in current_user_roles if role_object.role_name == role_name), None)
            if matching_role is None:
                flash("You do not have access to that page.", 'error')
                return redirect(url_for('wiki.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_list(path):
    file_dict = dict(name=path, files=[])
    try: file_list = os.listdir(path)
    except OSError: pass
    else:
        for filename in file_list:
            if not os.path.isdir(os.path.join(path, filename)):
                file_dict['files'].append(dict(name=filename))
    return file_dict


@bp.route('/')
@protect
def home():
    page = current_wiki.get('home')
    user_roles = RoleAssignmentManager(Database()).get_user_roles(current_user)
    user_admin_role = next((role_object for role_object in user_roles if role_object.role_name == "admin"), None)
    user_guest_role = next((role_object for role_object in user_roles if role_object.role_name == "guest"), None)

    if user_admin_role is not None:
        session['user_is_admin'] = True
    if user_guest_role is not None:
        session['user_is_guest'] = True
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
    return render_template('create.html', form=form, dir=config.UPLOAD_DIR)


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
    return render_template('editor.html', form=form, page=page, dir=config.UPLOAD_DIR, list=get_list(config.UPLOAD_DIR))

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
        new_url = form.url.data
        current_wiki.move(url, new_url)
        return redirect(url_for('wiki.display', url=new_url))
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
        return redirect(request.args.get("next") or url_for('wiki.home'))
    return render_template('login.html', form=form)


@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set_authenticated(False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.home'))


@bp.route('/user/')
@protect
def user_index():
    users = current_users.read_all()
    return render_template('users.html', users=users)


@bp.route('/user/create/', methods=['POST', 'GET'])
@protect
@requires_access_level('admin')
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
    all_roles = RoleManager(Database()).read_all()
    user_roles = RoleAssignmentManager(Database()).get_user_roles(user)
    roles_to_assign = set(all_roles).difference(user_roles)
    if len(roles_to_assign) == 0:
        roles_to_assign = None
    return render_template('user.html', user=user, user_roles=user_roles, roles_to_assign=roles_to_assign)


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
@requires_access_level('admin')
def roles():
    role_manager = RoleManager(Database())
    all_roles = role_manager.read_all()
    role_form = RoleForm()
    return render_template('roles.html', roles=all_roles, role_form=role_form)


@bp.route('/roles/create/', methods=['POST'])
@requires_access_level('admin')
def role_create():
    role_name = request.form['name']
    role_manager = RoleManager(Database())
    user_role = role_manager.create(role_name)
    if user_role is None:
        flash('Could not create role: "%s"' % role_name, 'error')
    return redirect(url_for('wiki.roles'))


@bp.route('/roles/delete/<string:role_name>/')
@requires_access_level('admin')
def role_delete(role_name):
    role_manager = RoleManager(Database())
    role_to_be_deleted = role_manager.read(role_name)
    deleted = role_manager.delete(role_to_be_deleted)
    if not deleted:
        flash('Could not delete role: "%s"' % role_name, 'error')
    if deleted:
        flash('Role: "%s" has been removed' % role_name, 'success')
    return redirect(url_for('wiki.roles'))


@bp.route('/role/assign/<int:user_id>/<string:role_name>/')
@requires_access_level('admin')
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
        if current_user.user_id == user_id and role.role_name == 'guest':
            session['user_is_guest'] = True
        if current_user.user_id == user_id and role.role_name == 'admin':
            session['user_is_admin'] = True
        flash('Role "%s" was assigned to user "%s"' % (role.role_name, user.user_name), 'success')
        return redirect(url_for('wiki.user_admin', user_name=user.user_name))
    return 'Could not assign role: "%s" to user id: "%s"' % (role_name, user_id)


@bp.route('/role/unassign/<int:user_id>/<string:role_name>/')
@requires_access_level('admin')
def role_unassign(user_id, role_name):
    user = current_users.read_id(user_id)
    user_roles = RoleAssignmentManager(Database()).get_user_roles(user)

    # Given a role name, checks if user has a role with that role name
    # returns None if role is not found
    role = next((role_object for role_object in user_roles if role_object.role_name == role_name), None)

    if role is not None:
        role_unassigned = RoleAssignmentManager(Database()).unassign_role_to_user(user, role)
        if current_user.user_id == user_id and role.role_name == 'admin':
            session['user_is_admin'] = False
        if current_user.user_id == user_id and role.role_name == 'guest':
            session['user_is_guest'] = False
        if role_unassigned:
            flash('Role "%s" was unassigned from user "%s"' % (role.role_name, user.user_name), 'success')
        elif not role_unassigned:
            flash('Could not assign role: "%s" to user: "%s"' % (role_name, user.user_name), 'error')
    elif role is None:
        flash('Could not find role: "%s" from user: "%s"' % (role_name, user.user_name), 'error')
    return redirect(url_for('wiki.user_admin', user_name=user.user_name))


@bp.route("/upload")
def upload():
    return render_template("upload.html")


@bp.route("/uploading", methods=["POST", "GET"])
def uploading():
    file = request.files['file']
    if file:
        file.save(os.path.join(current_app.config['UPLOAD_DIR'], secure_filename(file.filename)))
    return ""


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404