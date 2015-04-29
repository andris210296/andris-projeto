# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import urllib
from gaepermission import facade
from gaepermission.decorator import has_permission
from tekton.gae.middleware import Middleware

LOGIN_PATH = '/login'
LOGOUT_PATH = '/logout'


class LoggedUserMiddleware(Middleware):
    def set_up(self):
        user = facade.logged_user(self.handler.request).execute().result
        self.dependencies['_logged_user'] = user
        if user:
            self.dependencies['_logout_path'] = LOGOUT_PATH
            self.dependencies['_login_path'] = None
        else:
            return_path = urllib.urlencode({'ret_path': self.handler.request.path_qs})
            self.dependencies['_login_path'] = "%s?%s" % (LOGIN_PATH, return_path)
            self.dependencies['_logout_path'] = None


class PermissionMiddleware(Middleware):
    def set_up(self):
        fcn = self.dependencies['_fcn']
        user = self.dependencies['_logged_user']
        if not has_permission(user, fcn):
            if user is None:
                self.handler.redirect(self.dependencies['_login_path'])
            else:
                self.handler.response.status_int = 403
                self.handler.response.write('You have no access permission')
            return True