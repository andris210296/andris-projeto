# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie import facade
from gaecookie.decorator import is_csrf_secure
from os import urandom
from tekton.gae.middleware import Middleware

CSRF_CODE_KEY = '_csrf_code'


class CSRFInputToDependency(Middleware):
    def set_up(self):
        csrf_code = self.request_args.get(CSRF_CODE_KEY)
        if csrf_code:
            del self.request_args[CSRF_CODE_KEY]
            self.dependencies[CSRF_CODE_KEY] = csrf_code


class CSRFMiddleware(Middleware):
    def set_up(self):
        CSRF_TOKEN_COOKIE = 'XSRF-RANDOM'
        CSRF_ANGULAR_COOKIE = 'XSRF-TOKEN'
        CSRF_ANGULAR_AJAX_HEADER = 'X-XSRF-TOKEN'
        csrf_code = facade.retrive_cookie_data(self.handler.request, CSRF_TOKEN_COOKIE).execute().result
        if csrf_code:
            if self.handler.request.method != 'GET':
                angular_cookie_value = self.handler.request.headers.get(CSRF_ANGULAR_AJAX_HEADER)
                if csrf_code == angular_cookie_value:
                    return False
                form_input = self.dependencies.get(CSRF_CODE_KEY)
                if csrf_code == form_input:
                    return False
        else:
            csrf_code = urandom(16).encode('hex')
            facade.write_cookie(self.handler.response, CSRF_TOKEN_COOKIE, csrf_code).execute()
            self.handler.response.set_cookie(CSRF_ANGULAR_COOKIE, csrf_code)
        fcn = self.dependencies['_fcn']
        self.dependencies[CSRF_CODE_KEY] = csrf_code
        is_secure = is_csrf_secure(fcn)
        if is_secure:
            self.handler.response.status = '403 forbiden access'
            self.handler.response.write('Forbiden access')
        return is_secure