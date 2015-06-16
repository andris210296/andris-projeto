# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from tekton import router

_not_secure_path_set = set()


def is_csrf_secure_by_path(path):
    return path not in _not_secure_path_set


def is_csrf_secure(fcn):
    path = router.to_path(fcn)
    return is_csrf_secure_by_path(path)


def no_csrf(fcn):
    path = router.to_path(fcn)
    _not_secure_path_set.add(path)
    return fcn