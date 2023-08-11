from flask import render_template, redirect, url_for, abort, flash, request, \
    current_app
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries

from app import db
from app.base.views import BaseView
from app.customer import customer
from app.customer.forms import EditProfileForm, EditProfileAdminForm, PostForm
from app.models.LinkModel import Link
from app.models.MenuDb import Menu
from app.models.MockModel import Mock
from app.models.PermissionModel import Permission
from app.models.RoleModel import Role
from app.models.SysProgramDb import SysProgram
from app.models.UserLinkDb import UserLink
from app.models.UserModel import User
from app.common.components.decorators import admin_required, serialize


@customer.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['JC_MOCK_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@customer.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


# @customer.route('/', methods=['GET', 'POST'])
class IndexView(BaseView):

    decorators = [login_required]

    def dispatch_request(self):
        link_urls = []

        if not current_user.is_anonymous:
            common_links = UserLink.query.filter_by(user_link_user_id=current_user.id). \
                order_by(UserLink.user_link_link_count.desc()).limit(10)
            for common_link in common_links:
                link_url = Link.query.filter_by(link_id=common_link.user_link_link_id).one()
                link_urls.append(link_url)
        else:
            programs = SysProgram.query.filter_by(sys_program_group_id=8).all()
            programs = map(lambda x: x.sys_program_id, programs)
            link_urls = Link.query.filter(Link.link_type.in_(programs)).order_by(Link.link_id.desc()).limit(10)

        self.context.update({"link_urls": link_urls})
        return render_template(current_app.config["THEME_URL"] +'index.html', **self.context)


customer.add_url_rule('/', view_func=IndexView.as_view('index'))


class UserView(BaseView):
    decorators = [login_required]

    def dispatch_request(self, username):
        if username == current_user.username:
            user = User.query.filter_by(username=username).first_or_404()
            page = request.args.get('page', 1, type=int)
            # pagination = user.posts.order_by(User.timestamp.desc()).paginate(
            #     page, per_page=current_app.config['JC_MOCK_POSTS_PER_PAGE'],
            #     error_out=False)
            self.context.update({"user": user})
            return render_template(current_app.config["THEME_URL"] +'user.html', **self.context)
        else:
            return render_template(current_app.config["THEME_URL"] +'403.html')


customer.add_url_rule('/user/<username>', view_func=UserView.as_view('user'))


@customer.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.flush()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template(current_app.config["THEME_URL"] +'edit_profile.html', form=form)


@customer.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.flush()
        flash('The profile has been updated.')
        return redirect(url_for('customer.customer', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template(current_app.config["THEME_URL"] +'edit_profile.html', form=form, user=user)


@customer.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = User.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.flush()
        flash('The post has been updated.')
        return redirect(url_for('customer.post', id=post.id))
    form.body.data = post.body
    return render_template(current_app.config["THEME_URL"] +'edit_post.html', form=form)
