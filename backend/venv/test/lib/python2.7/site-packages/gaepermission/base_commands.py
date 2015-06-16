# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.model import Arc
from google.appengine.ext import ndb
from gaebusiness.business import Command, CommandParallel
from gaebusiness.gaeutil import ModelSearchCommand, SaveCommand
from gaecookie import facade
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import NodeSearch, SingleDestinationSearch
from gaepermission.model import MainUser, PendingExternalToMainUser, ExternalUser, ExternalToMainUser


def log_main_user_in(main_user, response, user_cookie):
    facade.write_cookie(response, user_cookie, {'id': main_user.key.id()}).execute()


class MainUserSearch(SingleDestinationSearch):
    arc_class = ExternalToMainUser


class GetMainUserByEmail(ModelSearchCommand):
    def __init__(self, email):
        super(GetMainUserByEmail, self).__init__(MainUser.query_email(email), 1)

    def do_business(self):
        super(GetMainUserByEmail, self).do_business()
        self.result = self.result[0] if self.result else None


class MainUserForm(ModelForm):
    _model_class = MainUser
    _include = [MainUser.email, MainUser.name, MainUser.groups, MainUser.locale, MainUser.timezone]


class SaveUserCmd(SaveCommand):
    _model_form_class = MainUserForm

    def handle_previous(self, command):
        self.result = command.result

    def __init__(self, **form_parameters):
        super(SaveUserCmd, self).__init__(**form_parameters)

    def do_business(self):
        if self.result is None:
            super(SaveUserCmd, self).do_business()


class UpdateUserGroups(NodeSearch):
    def __init__(self, user_id, groups):
        super(UpdateUserGroups, self).__init__(user_id)
        self.groups = groups

    def do_business(self):
        super(UpdateUserGroups, self).do_business()
        self.result.groups = self.groups

    def commit(self):
        return self.result


class FindMainUserFromExternalUserId(ModelSearchCommand):
    def __init__(self, external_user_class, external_id):
        super(FindMainUserFromExternalUserId,
              self).__init__(external_user_class.query_by_external_id(external_id), 1)
        self.external_user = None

    def do_business(self):
        super(FindMainUserFromExternalUserId, self).do_business()
        external_user = self.result[0] if self.result else None
        if external_user:
            self.result = MainUserSearch(external_user.key).execute().result
            self.external_user = external_user
        else:
            self.result = None


class CheckMainUserEmailConflict(CommandParallel):
    def __init__(self, external_user_class, external_id, email):
        super(CheckMainUserEmailConflict, self).__init__(GetMainUserByEmail(email),
                                                         FindMainUserFromExternalUserId(external_user_class,
                                                                                        external_id))
        self.external_user = None
        self.main_user_from_external = None
        self.main_user_from_email = None


    def do_business(self):
        super(CheckMainUserEmailConflict, self).do_business()
        self.result = True
        self.external_user = self[1].external_user
        self.main_user_from_external = self[1].result
        self.main_user_from_email = self[0].result

        if self.main_user_from_email and not self.main_user_from_external:
            self.result = False


class Login(CheckMainUserEmailConflict):
    def __init__(self, external_user_class, external_id, email, user_name, response, user_cookie):
        super(Login, self).__init__(external_user_class, external_id, email)
        self.user_name = user_name
        self.user_cookie = user_cookie
        self.response = response
        self._arc = None
        self.pending_link = None
        self.external_user_class = external_user_class
        self.external_id = external_id
        self.email = email


    def do_business(self):
        super(Login, self).do_business()

        # if no conflict
        if self.result:
            if self.external_user is None and self.main_user_from_external is None:
                self.external_user = self.external_user_class(external_id=self.external_id)
                self.main_user_from_external = MainUser(name=self.user_name,
                                                        email=self.email)
                external_user_key, main_user_key = ndb.put_multi([self.external_user, self.main_user_from_external])
                self._arc = ExternalToMainUser(origin=external_user_key, destination=main_user_key)
            log_main_user_in(self.main_user_from_external, self.response, self.user_cookie)
        else:
            if self.external_user is None:
                self.external_user = self.external_user_class(external_id=self.external_id)
                self.external_user.put()
            self.pending_link = PendingExternalToMainUser(external_user=self.external_user.key,
                                                          main_user=self.main_user_from_email.key)

    def commit(self):
        return [m for m in [self._arc, self.pending_link] if m]
