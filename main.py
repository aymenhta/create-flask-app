import argparse
from typing import Callable

from writer import (
    write_config,
    write_exts,
    write_init_core,
    write_package,
    write_requirements,
    write_run_file,
    write_utils,
)


def main():
    args_parser = argparse.ArgumentParser(description="this is a description")
    args_parser.add_argument("-o", "--output", help="name of the project")
    args_parser.add_argument("-d", "--dir", help="where to create the project")
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
        f"{core_pkg_path}/utils.py": write_utils,
    }
    write_package(core_pkg_path, files)


if __name__ == "__main__":
    main()
