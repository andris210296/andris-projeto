# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import users
from tekton import router

_security_permission_group_map = {}


class _MsgHelper(object):
    '''
    Class that aways returns True for in operation
    '''

    def __init__(self, msg):
        self.msg = msg

    def __unicode__(self):
        return self.msg


_login_required = _MsgHelper('Login Required')
_login_not_required_helper = _MsgHelper('Login not Required')


def permissions(*groups):
    def decorator(fcn):
        path = router.to_path(fcn)
        _security_permission_group_map[path] = frozenset(groups)
        return fcn

    return decorator


def login_not_required(fcn):
    path = router.to_path(fcn)
    _security_permission_group_map[path] = _login_not_required_helper
    return fcn


def login_required(fcn):
    path = router.to_path(fcn)
    _security_permission_group_map[path] = _login_required
    return fcn


def get_groups_by_path(path):
    return _security_permission_group_map.get(path)


def get_groups(fcn):
    path = router.to_path(fcn)
    return get_groups_by_path(path)


def has_permission(user, fcn):
    groups = get_groups(fcn)

    if groups is _login_not_required_helper:
        return True
    if user and groups is _login_required:
        return True

    if user and groups:
        for g in user.groups:
            if g in groups:
                return True

    return users.is_current_user_admin()
