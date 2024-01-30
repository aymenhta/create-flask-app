import os
from typing import Callable


def write_package(pkg_path: str, pkg_files: dict[str, Callable]):
    os.mkdir(pkg_path)
    write_pkg_files(pkg_files)


def write_pkg_files(files_with_func: dict[str, Callable]):
    for f, fn in files_with_func.items():
        with open(f, "w+", encoding="utf-8") as w:
            fn(w)


def write_requirements(w):
    packages: list[tuple(str, str)] = [
        ("alembic", "1.9.4"),
        ("bcrypt", "4.0.1"),
        ("black", "23.1.0"),
        ("click", "8.1.3"),
        ("colorama", "0.4.6"),
        ("dnspython", "2.3.0"),
        ("email-validator", "1.3.1"),
        ("Flask", "2.2.3"),
        ("Flask-Bcrypt", "1.0.1"),
        ("Flask-Login", "0.6.2"),
        ("Flask-Migrate", "4.0.4"),
        ("Flask-SQLAlchemy", "3.0.3"),
        ("Flask-WTF", "1.1.1"),
        ("greenlet", "2.0.2"),
        ("idna", "3.4"),
        ("importlib-metadata", "6.0.0"),
        ("itsdangerous", "2.1.2"),
        ("Jinja2", "3.1.2"),
        ("Mako", "1.2.4"),
        ("MarkupSafe", "2.1.2"),
        ("mypy-extensions", "1.0.0"),
        ("packaging", "23.0"),
        ("pathspec", "0.11.0"),
        ("platformdirs", "3.1.1"),
        ("python-dotenv", "0.21.1"),
        ("SQLAlchemy", "2.0.4"),
        ("tomli", "2.0.1"),
        ("typing_extensions", "4.5.0"),
        ("Werkzeug", "2.2.3"),
        ("WTForms", "3.0.1"),
        ("zipp", "3.14.0"),
    ]
    [w.write(f"{pkg[0]}=={pkg[1]}\n") for pkg in packages]


def write_run_file(w):
    w.write("from core import app\n")
    w.write("\n")
    w.write("\n")
    w.write("if __name__ == '__main__':\n")
    w.write("\tapp.run(debug=True)")


def write_init_core(w):
    w.write("from flask import Flask\n")
    w.write("\n")
    w.write("from .config import Config\n")
    w.write("from .exts import (\n")
    w.write("\tdb,\n")
    w.write("\tmigrate,\n")
    w.write("\tlogin_manager,\n")
    w.write("\tbcrypt,\n")
    w.write("\tcsrf,\n")
    w.write(")\n")
    w.write("\n")
    w.write("\n")
    w.write("def create_app(config_class=Config) -> Flask:\n")
    w.write("\tflask_app: Flask = Flask(__name__)\n")
    w.write("\tflask_app.config.from_object(config_class)\n")
    w.write("\n")
    w.write("\t# init extensions\n")
    w.write("\tdb.init_app(flask_app)\n")
    w.write("\tcsrf.init_app(flask_app)\n")
    w.write("\tmigrate.init_app(flask_app, db, render_as_batch=True)\n")
    w.write("\tbcrypt.init_app(flask_app)\n")
    w.write("\tlogin_manager.init_app(flask_app)\n")
    w.write("\n")
    w.write("\t# import routes\n")
    w.write("\tfrom .store import store\n")
    w.write("\tfrom .auth import auth\n")
    w.write("\tfrom .dashboard import dashboard\n")
    w.write("\n")
    w.write("\t# register blueprints\n")
    w.write("\tflask_app.register_blueprint(store)\n")
    w.write("\tflask_app.register_blueprint(auth)\n")
    w.write("\tflask_app.register_blueprint(dashboard)\n")
    w.write("\n")
    w.write("\treturn flask_app\n")
    w.write("\n")
    w.write("\n")
    w.write("app: Flask = create_app()")


def write_utils(w):
    w.write("import os\n")
    w.write("import secrets\n")
    w.write("\n")
    w.write("from flask import current_app\n")
    w.write("\n")
    w.write("\n")
    w.write("def save_pic(form_picture, folder_path: str) -> str:\n")
    w.write("\trandom_hex = secrets.token_hex(8)\n")
    w.write("\t_, f_ext = os.path.splitext(form_picture.filename)\n")
    w.write("\t# rename it\n")
    w.write("\tpicture_filename = random_hex + f_ext\n")
    w.write("\t# path\n")
    w.write(
        "\tpicture_path = os.path.join(current_app.root_path, folder_path, picture_filename)\n"
    )
    w.write("\t# save it\n")
    w.write("\tform_picture.save(picture_path)\n")
    w.write("\treturn picture_filename")


def write_config(w):
    w.write("import os\n")
    w.write("from dotenv import load_dotenv, find_dotenv\n")
    w.write("\n")
    w.write("load_dotenv(find_dotenv())\n")
    w.write("\n")
    w.write("\n")
    w.write("class Config(object):\n")
    w.write("\tSECRET_KEY = os.environ.get('SECRET_KEY')\n")
    w.write("\tSQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')\n")
    w.write("\tSQLALCHEMY_TRACK_MODIFICATIONS = False\n")
    w.write("\tSQLALCHEMY_ECHO = True  # write generated sql at the console")


def write_exts(w):
    w.write("from flask_sqlalchemy import SQLAlchemy\n")
    w.write("from flask_login import LoginManager\n")
    w.write("from flask_migrate import Migrate\n")
    w.write("from flask_bcrypt import Bcrypt\n")
    w.write("from flask_wtf import CSRFProtect\n")
    w.write("\n")
    w.write("\n")
    w.write("db: SQLAlchemy = SQLAlchemy()\n")
    w.write("migrate: Migrate = Migrate()\n")
    w.write("login_manager: LoginManager = LoginManager()\n")
    w.write("login_manager.login_view = 'auth.login'\n")
    w.write("login_manager.login_message_category = 'info'\n")
    w.write("bcrypt: Bcrypt = Bcrypt()\n")
    w.write("csrf: CSRFProtect = CSRFProtect()")
