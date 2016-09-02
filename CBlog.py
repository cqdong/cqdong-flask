from app import create_app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manager, Server
from app.models import Post, User, TestMptt, Comment
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, posts=Post, users=User, testmptts=TestMptt, comments=Comment)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('runserver', Server(host='127.0.0.1', port=5000, use_debugger=True))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
