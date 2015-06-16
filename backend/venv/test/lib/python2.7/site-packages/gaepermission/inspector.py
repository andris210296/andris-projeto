# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import importlib
import inspect
from gaecookie.decorator import is_csrf_secure_by_path
from gaepermission.decorator import get_groups_by_path
import os
from tekton import router


def _paths_helper(base_path, prefix_path):
    prefix_len = len(prefix_path) + 1
    for dirpath, dirnames, filenames in os.walk(base_path, False):
        package = dirpath[prefix_len:].replace(r'/', '.').replace(os.path.sep, '.')  # second replace due windows
        pyfile_names = (f[:-3] for f in filenames if f.endswith('.py') and f != '__init__.py')
        for fname in pyfile_names:
            module_name = '.'.join((package, fname))
            module = importlib.import_module(module_name)
            for item_name in dir(module):
                item = getattr(module, item_name)
                if inspect.isfunction(item):
                    path = router.to_path(item)
                    if path.startswith('/'):
                        yield path


def web_paths(base_package):
    module = importlib.import_module(base_package)
    base_path = os.path.dirname(module.__file__)
    prefix_path = os.path.join(base_path, '..' * (base_package.count(r'.') + 1))
    prefix_path = os.path.abspath(prefix_path)
    return _paths_helper(base_path, prefix_path)


class PathInfo(object):
    def __init__(self, path):
        self.csrf = is_csrf_secure_by_path(path)
        g = get_groups_by_path(path)
        if g is None:
            g = 'SYS_OWNER'
        if isinstance(g, frozenset):
            g = ', '.join(g)
        self.groups = unicode(g)
        self.path = path


def web_paths_security_info(base_package):
    for path in web_paths(base_package):
        yield PathInfo(path)




