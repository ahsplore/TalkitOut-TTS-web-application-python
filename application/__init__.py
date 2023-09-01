from flask import Flask
from flask_dropzone import Dropzone
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_session import Session

db = SQLAlchemy()
DB_NAME = "database.db"

app = Flask(__name__)


def create_app():
    app.config['SECRET_KEY'] = 'abcv6QT@a83iufcq92iU#$*63nmJDYE8Fdbcusv-=U45&kgBUGK'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


def create_database(app):
    if not path.exists('application/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


dir_path = path.dirname(path.realpath(__file__))

app.config.update(
    UPLOADED_PATH=path.join(dir_path, 'static/uploaded_files/'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=1,
    AUDIO_FILE_UPLOAD=path.join(dir_path, 'static/audio_files/')
)

app.config['DROPZONE_REDIRECT_VIEW'] = 'auth.decoded'

dropzone = Dropzone(app)
