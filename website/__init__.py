from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restx import Api
import os

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    # -------------------
    # CONFIG
    # -------------------
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SECRET_KEY'] = os.getenv('secret_key', 'defaultsecret')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # -------------------
    # INIT EXTENSIONS
    # -------------------
    db.init_app(app)

    # -------------------
    # SWAGGER / API
    # -------------------
    api = Api(
        app,
        version="1.0",
        title="Notes API",
        description="Notes App REST API Documentation",
        doc="/docs"
    )

    from .api.notes import api as notes_ns

    api.add_namespace(notes_ns, path="/api/notes")

    # -------------------
    # BLUEPRINTS
    # -------------------
    from .views import views
    from .auth import auth

    with app.app_context():
        db.create_all()

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # -------------------
    # LOGIN MANAGER
    # -------------------
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_page'
    login_manager.init_app(app)

    from .models import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    return app