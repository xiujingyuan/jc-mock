#!/usr/bin/env python

import os
import shutil

from flask_login import current_user

from app import create_app, db
from app.models.MenuDb import Menu
from app.models.MockModel import Mock
from app.models.PageViewDb import PageView
from flask_mail import Mail
from flask import request

from app.models.SysOrganizationDb import SysOrganization
from app.models.SysProgramDb import SysProgram
from app.models.UserModel import User
from app.models.RoleModel import Role
from app.models.PermissionModel import Permission
from app.models.LinkModel import Link
from app.tasks.common_task.calc_count import calc_count_task
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.common.config.config import config
from raven.contrib.flask import Sentry


COV = None

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

sentry = Sentry(app, dsn=app.config['SENTRY_DSN'])
manager = Manager(app)
migrate = Migrate(app, db)
mail = Mail(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role,
                Permission=Permission, Link=Link, Mock=Mock, PageView=PageView,
                Menu=Menu, SysOrganization=SysOrganization,
                SysProgram=SysProgram)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

base_dir = os.path.abspath(os.path.dirname(__file__))
base_config_url = os.path.join(base_dir, "environment")
dev_config_url = os.path.join(base_config_url, "dev", "config.py")
test_config_url = os.path.join(base_config_url, "test", "config.py")
prod_config_url = os.path.join(base_config_url, "prod", "config.py")
dst_config_url = os.path.join(base_dir, "app", "common", "config", "config.py")


@app.after_request
def release_db(response):
    ip = request.remote_addr
    req_path = request.path
    if '/common/request' in req_path:
        print(request.json, response.json)
        calc_count_task.delay(ip, request.json, request.method, current_user.username if hasattr(current_user, 'username') else 'admin', response.json)
    return response


@manager.command
def init():
    input_init_str = "Please select the environment you want to init:\r\n"
    aevalible_index_dict = {}
    for index, env in enumerate(list(config.keys())[:-1]):
        input_init_str += "{0}:{1}\r\n".format(index+1, env)
        aevalible_index_dict[str(index+1)] = env

    while True:
        select_env = input(input_init_str)
        if select_env in list(aevalible_index_dict.keys()):
            break

    select_env = int(select_env)
    while True:
        input_over_str = "Do you over the config?|Yes|No"
        select_str = input(input_over_str)
        if select_str.lower() == "yes":
            src = dev_config_url
            if select_env == 2:
                src = test_config_url
            elif select_env == 3:
                src = prod_config_url
            dst = dst_config_url
            shutil.copyfile(src, dst)
            print("Over file success!")
            break
        elif select_str.lower() == "no":
            break


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    from app.models.RoleModel import Role

    # migrate database to latest revision
    upgrade()

    # create user roles
    Role.insert_roles()

    # # create self-follows for all users
    # User.add_self_follows()


if __name__ == '__main__':
    manager.run()
