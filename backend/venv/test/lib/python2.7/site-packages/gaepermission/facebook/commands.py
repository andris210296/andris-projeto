# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json

from google.appengine.api import memcache
from google.appengine.ext import ndb
from gaebusiness.business import Command

from gaebusiness.gaeutil import ModelSearchCommand, UrlFetchCommand
from gaecookie import facade
from gaepermission.base_commands import FindMainUserFromExternalUserId, CheckMainUserEmailConflict, Login, \
    ExternalToMainUser
from gaepermission.facebook.model import FacebookApp
from gaepermission.model import FacebookUser, ExternalToMainUser, MainUser


class GetFacebookApp(ModelSearchCommand):
    def __init__(self):
        super(GetFacebookApp, self).__init__(FacebookApp.query(), 1)

    def do_business(self):
        super(GetFacebookApp, self).do_business()
        if self.result:
            self.result = self.result[0]
        else:
            self.result = None


class SaveOrUpdateFacebookApp(GetFacebookApp):
    def __init__(self, id=None, token=None):
        super(SaveOrUpdateFacebookApp, self).__init__()
        self.token = token
        self.id = id

    def do_business(self):
        super(SaveOrUpdateFacebookApp, self).do_business()
        if not self.result:
            self.result = FacebookApp()
        else:
            memcache.delete(self._cache_key())
        if self.id:
            self.result.app_id = self.id
        if self.token:
            self.result.token = self.token

    def commit(self):
        return self.result


class FetchFacebook(UrlFetchCommand):
    def __init__(self, token):
        super(FetchFacebook, self).__init__('https://graph.facebook.com/v2.0/me',
                                            {'fields': 'id,email,name',
                                             'access_token': token})
        self._to_commit = None

    def do_business(self):
        super(FetchFacebook, self).do_business()
        if not self.errors:
            self.result = json.loads(self.result.content)


class LogFacebookUserIn(Command):
    def __init__(self, token, response, user_cookie_name):
        super(LogFacebookUserIn, self).__init__()
        self._fetch_facebook = FetchFacebook(token)
        self._login_cmd = None
        self.user_cookie_name = user_cookie_name
        self.response = response
        self.pending_link = None
        self.external_user = None
        self.main_user_from_external = None
        self.main_user_from_email = None

    def set_up(self):
        self._fetch_facebook.set_up()


    def do_business(self):
        self._fetch_facebook.do_business()
        self.errors.update(self._fetch_facebook.errors)
        if not self.errors:
            dct = self._fetch_facebook.result
            self._login_cmd = Login(FacebookUser,
                                    dct['id'],
                                    dct['email'],
                                    dct['name'],
                                    self.response,
                                    self.user_cookie_name)
            self._login_cmd.set_up()
            self._login_cmd.do_business()

    def commit(self):
        if self._login_cmd:
            self.result = self._login_cmd.result
            self.pending_link = self._login_cmd.pending_link
            self.external_user = self._login_cmd.external_user
            self.main_user_from_external = self._login_cmd.main_user_from_external
            self.main_user_from_email = self._login_cmd.main_user_from_email
            return self._login_cmd.commit()

