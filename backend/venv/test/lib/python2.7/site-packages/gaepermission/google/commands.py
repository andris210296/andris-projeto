# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from gaepermission.base_commands import Login
from gaepermission.model import GoogleUser


class GoogleLogin(Login):
    def __init__(self, google_api_user, response, user_cookie):
        super(GoogleLogin, self).__init__(GoogleUser,
                                          google_api_user.user_id(),
                                          google_api_user.email(),
                                          google_api_user.nickname(),
                                          response,
                                          user_cookie)

        []