# -*- coding:utf-8 -*-
from app import create_app,db
import os
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate,MigrateCommand
from app.models import User,Role,Permission,Post,Follow,Comment,Category
import sys

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True,include='app/*')
    COV.start()

reload(sys)
sys.setdefaultencoding('utf-8')


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app,User=User,db=db,Role=Role,
                Follow=Follow,Permission=Permission,Post=Post,Comment=Comment,Category=Category)
manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)


@manager.command
def test(coverage=False):
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable,[sys.executable]+sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir,'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version:file://%s/index.html' % covdir)
        COV.erase()

@manager.command
def profile(length=25,profile_dir=None):
    "分析器下运行程序"
    from werkzeug.contrib.prifiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app,restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    from flask.ext.migrate import upgrade
    from app.models import  Role,User

    #migrate database to  the latest version
    #upgrade()

    #create roles
    Role.insert_roles()

    #create Categories
    Category.insert_categories()

    #create self_follows
    User.add_self_follows()

if __name__ == '__main__':
    manager.run()