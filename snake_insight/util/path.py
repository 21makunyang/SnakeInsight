import os
import sys

root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
prefix = 'SI.'


def get_relative_path(abs_path: str) -> str:
    return os.path.relpath(abs_path, root_path) if abs_path.startswith(root_path) else abs_path


def file_path_to_module_path(path: str) -> str:
    return prefix + path.replace('\\', '.')


def to_module_path(*, abs_path: str = None, rel_path: str = None) -> str:
    if rel_path is not None:
        return file_path_to_module_path(path=rel_path)
    elif abs_path is not None:
        return file_path_to_module_path(get_relative_path(abs_path=abs_path))
    else:
        raise Exception('Parameter abs_path and parameter rel_path cannot be both None.')
