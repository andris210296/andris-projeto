# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json

from google.appengine.api import memcache
from google.appengine.ext import ndb
from gaebusiness.business import CommandParallel

from gaebusiness.gaeutil import ModelSearchCommand, UrlFetchCommand
from gaecookie import facade
from gaegraph.business_base import SingleDestinationSearch
from gaepermission.base_commands import GetMainUserByEmail, ExternalToMainUser, MainUserSearch
from gaepermission.model import MainUser, ExternalToMainUser, PasswordlessUser
from gaepermission.passwordless.model import PasswordlessApp


class GetApp(ModelSearchCommand):
    def __init__(self):
        super(GetApp, self).__init__(PasswordlessApp.query(), 1)

    def do_business(self):
        super(GetApp, self).do_business()
        if self.result:
            self.result = self.result[0]
        else:
            self.result = None


class SaveOrUpdateApp(GetApp):
    def __init__(self, id=None, token=None):
        super(SaveOrUpdateApp, self).__init__()
        self.token = token
        self.id = id

    def do_business(self):
        super(SaveOrUpdateApp, self).do_business()
        if not self.result:
            self.result = PasswordlessApp()
        else:
            memcache.delete(self._cache_key())
        if self.id:
            self.result.app_id = self.id
        if self.token:
            self.result.token = self.token

    def commit(self):
        return self.result


class SengLoginEmail(GetApp):
    def __init__(self, email, return_url, lang, url_passwordless_login):
        super(SengLoginEmail, self).__init__()
        self.url_passwordless_login = url_passwordless_login
        self.email = email
        self.return_url = return_url
        self.lang = lang


    def do_business(self):
        super(SengLoginEmail, self).do_business()
        app = self.result
        if app:
            fetch_command = UrlFetchCommand(self.url_passwordless_login,
                                            {'email': self.email,
                                             'app_id': app.app_id,
                                             'token': app.token,
                                             'hook': self.return_url,
                                             'lang': self.lang},
                                            method='POST')
            fetch_command.execute()
        else:
            self.add_error('app_data', 'Must save Passwordless App Credentials before login calls')


class GetPasswordlessUser(ModelSearchCommand):
    def __init__(self, passwordless_id):
        super(GetPasswordlessUser, self).__init__(PasswordlessUser.query_by_external_id(passwordless_id), 1)

    def do_business(self):
        super(GetPasswordlessUser, self).do_business()
        self.result = self.result[0] if self.result else None


class PasswordlessDetailCheck(GetApp):
    def __init__(self, ticket, detail_url):
        super(PasswordlessDetailCheck, self).__init__()
        self.detail_url = detail_url
        self.ticket = ticket
        self._to_commit = None

    def do_business(self):
        super(PasswordlessDetailCheck, self).do_business()
        if not self.errors:
            app = self.result
            self.result = None
            fetch_cmd = UrlFetchCommand(self.detail_url,
                                        {'ticket': self.ticket, 'app_id': app.app_id, 'token': app.token},
                                        'POST').execute()
            self.errors.update(fetch_cmd.errors)
            if not self.errors:
                dct = json.loads(fetch_cmd.result.content)
                cmd_parallel = CommandParallel(GetMainUserByEmail(dct['email']), GetPasswordlessUser(dct['id']))
                cmd_parallel.execute()
                main_user, passwordless_user = cmd_parallel[0].result, cmd_parallel[1].result
                if passwordless_user:
                    main_user = MainUserSearch(passwordless_user).execute().result
                elif main_user:
                    passwordless_user_key = PasswordlessUser(external_id=dct['id']).put()
                    self._to_commit = ExternalToMainUser(origin=passwordless_user_key, destination=main_user.key)
                else:
                    main_user = MainUser(name=dct['email'], email=dct['email'])
                    passwordless_user = PasswordlessUser(external_id=dct['id'])
                    ndb.put_multi([main_user, passwordless_user])
                    self._to_commit = ExternalToMainUser(origin=passwordless_user.key, destination=main_user.key)
                self.result = main_user

    def commit(self):
        return self._to_commit


class Login(PasswordlessDetailCheck):
    def __init__(self, ticket, response, user_cookie_name, detail_url):
        super(Login, self).__init__(ticket, detail_url)
        self.response = response
        self.user_cookie_name = user_cookie_name

    def do_business(self):
        super(Login, self).do_business()
        facade.write_cookie(self.response, self.user_cookie_name, {'id': self.result.key.id()}).execute()



