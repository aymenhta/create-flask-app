import argparse
from typing import Callable

from writer import (
    write_about_html,
    write_base_html,
    write_bp_forms,
    write_bp_index_html,
    write_bp_init,
    write_bp_routes,
    write_config,
    write_exts,
    write_init_core,
    write_main_css,
    write_main_js,
    write_models,
    write_package,
    write_requirements,
    write_run_file,
    write_utils,
)

# python main.py -o flaskr -d . -b main
# TODO: environment variables
def main():
    parser = argparse.ArgumentParser(description="this is a description")
    parser.add_argument("-o", "--output", help="name of the project")
    parser.add_argument("-d", "--dir", help="where to create the project")
    parser.add_argument("-b", "--blueprints", nargs='+', default=[], help="create another blueprint")

    args = parser.parse_args()
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
    if len(args.blueprints) < 1:
        args.blueprints.append("main")
        args.blueprints.append("auth")
    for bp in args.blueprints:
        bp_dir = f"{core_pkg_path}/{bp}"
        files: dict[str, Callable] = {
            f"{bp_dir}/__init__.py": write_bp_init,
            f"{bp_dir}/routes.py": write_bp_routes,
            f"{bp_dir}/forms.py": write_bp_forms,
        }

        templs: dict[str, Callable] = {
            f"{bp_dir}/templates/{bp}/index.html": write_bp_index_html,
        }

        write_package(bp_dir, files, is_blueprint=True, templates=templs)


if __name__ == "__main__":
    main()
