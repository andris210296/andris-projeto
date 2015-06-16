# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import Command
from gaecookie.security import SignCmd, RetrieveCmd


class DeleteCookie(Command):
    def __init__(self, response, cookie_name):
        super(DeleteCookie, self).__init__()
        self.cookie_name = cookie_name
        self.response = response


    def do_business(self, stop_on_error=True):
        self.response.delete_cookie(self.cookie_name)


class WriteCookie(SignCmd):
    def __init__(self, response, name, obj):
        super(WriteCookie, self).__init__(name, obj)
        self.response = response

    def do_business(self, stop_on_error=False):
        super(WriteCookie, self).do_business(stop_on_error)
        if self.result:
            self.response.set_cookie(self.name, self.result, httponly=True, overwrite=True)


class RetrieveCookieData(RetrieveCmd):
    def __init__(self, request, cookie_name, max_age=604800):
        signed = request.cookies.get(cookie_name)
        super(RetrieveCookieData, self).__init__(cookie_name, signed, max_age)