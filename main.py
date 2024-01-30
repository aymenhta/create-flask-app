import argparse
from typing import Callable

from writer import (
    write_about_html,
    write_base_html,
    write_bp_init,
    write_bp_routes,
    write_config,
    write_exts,
    write_init_core,
    write_login_html,
    write_main_css,
    write_main_js,
    write_models,
    write_package,
    write_register_html,
    write_requirements,
    write_run_file,
    write_utils,
)

# python main.py -o flaskr -d . -b main
def main():
    args_parser = argparse.ArgumentParser(description="this is a description")
    args_parser.add_argument("-o", "--output", help="name of the project")
    args_parser.add_argument("-d", "--dir", help="where to create the project")
    args_parser.add_argument("-b", "--blueprint", help="create another blueprint")
    args = args_parser.parse_args()
    if not args.dir:
        args.dir = "."
    if not args.output:
        print("name of the folder should be provided")
        exit(1)

    # create root directory
    root_dir = f"{args.dir}/{args.output}"
    files = {
        f"{root_dir}/requirements.txt": write_requirements,
        f"{root_dir}/run.py": write_run_file,
    }
    write_package(root_dir, files)

    # write the core package
    core_pkg_path = root_dir + "/core"
    files: dict[str, Callable] = {
        f"{core_pkg_path}/__init__.py": write_init_core,
        f"{core_pkg_path}/exts.py": write_exts,
        f"{core_pkg_path}/config.py": write_config,
        f"{core_pkg_path}/models.py": write_models,
        f"{core_pkg_path}/utils.py": write_utils,
    }
    templs: dict[str, Callable] = {
        f"{core_pkg_path}/templates/base.html": write_base_html,
        f"{core_pkg_path}/templates/about.html": write_about_html,
    }
    static: dict[str, Callable] = {
        f"{core_pkg_path}/static/css/main.css": write_main_css,
        f"{core_pkg_path}/static/js/main.js": write_main_js,
    }
    write_package(core_pkg_path, files, templates=templs, statics=static)

    # generate blueprints
    if not args.blueprint:
        args.blueprint = "auth"
    bp_dir = f"{core_pkg_path}/{args.blueprint}"
    files: dict[str, Callable] = {
        f"{bp_dir}/__init__.py": write_bp_init,
        f"{bp_dir}/routes.py": write_bp_routes,
    }

    templs: dict[str, Callable] = {
        f"{bp_dir}/templates/{args.blueprint}/login.html": write_login_html,
        f"{bp_dir}/templates/{args.blueprint}/register.html": write_register_html,
    }

    write_package(bp_dir, files, is_blueprint=True, templates=templs)


if __name__ == "__main__":
    main()
