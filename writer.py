import os
from typing import Callable, Optional


def write_package(
    pkg_path: str,
    pkg_files: dict[str, Callable],
    templates: Optional[dict[str, Callable]] = None,
    statics: Optional[dict[str, Callable]] = None,
    is_blueprint: bool = False,
):
    # create the package directrory
    os.mkdir(pkg_path)
    # if the specified package is a blueprint, then pass the blueprint name to the write function
    if not is_blueprint:
        write_pkg_files(pkg_files)
    else:
        bp_name = pkg_path.split("/")[-1]
        write_pkg_files(pkg_files, pkg=bp_name)

    if statics:
        dirs = [f"{pkg_path}/static", f"{pkg_path}/static/css", f"{pkg_path}/static/js"]
        [os.mkdir(s_dir) for s_dir in dirs]
        write_pkg_files(statics)

    if templates:
        os.mkdir(f"{pkg_path}/templates")
        if is_blueprint:
            os.mkdir(f"{pkg_path}/templates/{bp_name}")
        write_pkg_files(templates)


def write_pkg_files(files_with_func: dict[str, Callable], pkg: str = ""):
    for f, fn in files_with_func.items():
        with open(f, "w+", encoding="utf-8") as w:
            fn(w, pkg)


def write_requirements(w, *args):
    w.write(
        """alembic==1.9.4
bcrypt==4.0.1
black==23.1.0
click==8.1.3
colorama==0.4.6
dnspython==2.3.0
email-validator==1, *args.3.1
Flask==2.2.3
Flask-Bcrypt==1.0.1
Flask-Login==0.6.2
Flask-Migrate==4.0.4
Flask-SQLAlchemy==3.0.3
Flask-WTF==1.1.1
greenlet==2.0.2
idna==3.4
importlib-metadata==6.0.0
itsdangerous==2.1.2
Jinja2==3.1.2
Mako==1.2.4
MarkupSafe==2.1.2
mypy-extensions==1.0.0
packaging==23.0
pathspec==0.11.0
platformdirs==3.1.1
python-dotenv==0.21.1
SQLAlchemy==2.0.4
tomli==2.0.1
typing_extensions==4.5.0
Werkzeug==2.2.3
WTForms==3.0.1
zipp==3.14.0"""
    )


def write_run_file(w, *args):
    w.write(
        """from core import app


if __name__ == '__main__':
	app.run(debug=True)"""
    )


def write_init_core(w, *args):
    w.write(
        """from flask import Flask

from .config import Config
from .exts import (
	db,
	migrate,
	login_manager,
	bcrypt,
	csrf,
)


def create_app(config_class=Config) -> Flask:
	flask_app: Flask = Flask(__name__)
	flask_app.config.from_object(config_class)

	# init extensions
	db.init_app(flask_app)
	csrf.init_app(flask_app)
	migrate.init_app(flask_app, db, render_as_batch=True)
	bcrypt.init_app(flask_app)
	login_manager.init_app(flask_app)

	# import routes
	from .auth import auth

	# register blueprints
	flask_app.register_blueprint(auth)

	return flask_app


app: Flask = create_app()"""
    )


def write_models(w, *args):
    w.write(
        """from datetime import datetime
from flask_login import UserMixin
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from core import db, login_manager
            
@login_manager.user_loader
def load_user(user_id):  # A Func to get a user by id
    return User.query.get(int(user_id))


user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
)

            
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(6), unique=True, nullable=False)
    email = sa.Column(sa.String(120), unique=True, nullable=False)
    password = sa.Column(sa.String(60), nullable=False)
    gender = sa.Column(sa.String(10), nullable=False, default="Male")
    date_joined = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    profile_file = sa.Column(sa.String(20), nullable=False, default="default.jpg")
    roles = db.relationship(
        "Role",
        secondary=user_roles,
        lazy="subquery",
        backref=db.backref("users", lazy=True),
    )

    @property
    def is_admin(self) -> bool:
        for role in self.roles:
            if role.name == "admin":
                return True
        return False

    def __repr__(self):
        return f"<User : {self.id}, {self.email}, {self.username}, {self.date_joined}"
            

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Role : {self.id}, {self.name}"
"""
    )


def write_bp_init(w, bp: str):
    w.write(f"from .routes import {bp}")


def write_bp_routes(w, bp: str):
    w.write(
        f"""from flask import Blueprint, flash, redirect, render_template, request, url_for

from core import db

{bp} = Blueprint("{bp}", __name__, template_folder="templates/auth")


@{bp}.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", title="index")
"""
    )


def write_utils(w, *args):
    w.write(
        """import os, secrets

from flask import current_app
            
            
def save_pic(form_picture, folder_path: str) -> str:
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    # rename it
    picture_filename = random_hex + f_ext
    # path
    picture_path = os.path.join(current_app.root_path, folder_path, picture_filename)
    # save it
    form_picture.save(picture_path)
    # return filename
    return picture_filename
"""
    )


def write_config(w, *args):
    w.write(
        """import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_ECHO = True  # write generated sql at the console"""
    )


def write_exts(w, *args):
    w.write(
        """from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect


db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()
login_manager: LoginManager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
bcrypt: Bcrypt = Bcrypt()
csrf: CSRFProtect = CSRFProtect()"""
    )


def write_base_html(w, *args):
    w.write(
        """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link
      rel="stylesheet"
      href="{{ url_for('static', filename='css/main.css') }}"
    />
    
</head>
<body>
    {% include './partials/header.html' %}

    <!-- Message Flashing -->
    {% if current_user.is_authenticated %}
        {% include './partials/flash.html' %}  
    {% endif %}

    {% block content %}
    
    {% endblock %}
</body>
</html>"""
    )


def write_about_html(w, *args):
    w.write(
        """{% extends 'base.html' %}
{% block content %}
    <h1>About us</h1>
{% endblock %}"""
    )


def write_login_html(w, *args):
    w.write(
        """{% extends 'base.html' %}
{% block content %}
    <h1>Login</h1>
{% endblock %}"""
    )


def write_register_html(w, *args):
    w.write(
        """{% extends 'base.html' %}
{% block content %}
    <h1>Register</h1>
{% endblock %}"""
    )


def write_main_css(w, *args):
    w.write(
        """* {
	margin: 0;
	padding: 0;
	box-sizing: border-box;
}

.container {
	margin: 0 auto;
	width: 85%;
	max-width: 1920px;
}"""
    )


def write_main_js(w, *args):
    w.write("console.log('Hello, world!')")
