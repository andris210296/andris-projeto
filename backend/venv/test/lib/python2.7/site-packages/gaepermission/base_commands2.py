# -*- coding: utf-8 -*-


from __future__ import absolute_import, unicode_literals


# This class should be on base_commands, but it would cause circular dependency
from gaebusiness.business import CommandParallel
from gaegraph.business_base import NodeSearch, SingleDestinationSearch
from gaepermission.base_commands import ExternalToMainUser, MainUserSearch
from gaepermission.passwordless.commands import Login





def _is_there_a_link_already(pending_model):
    return MainUserSearch(pending_model.external_user).execute().result


def _is_pending_user_same_as_loging_in(main_user, pending_model):
    return pending_model.main_user == main_user.key


def _should_create_link(main_user, pending_model):
    return pending_model and _is_pending_user_same_as_loging_in(main_user,
                                                                pending_model) and not _is_there_a_link_already(
        pending_model)


class LoginCheckingEmail(CommandParallel):
    def __init__(self, pending_id, ticket, response, user_cookie_name, detail_url):
        super(LoginCheckingEmail, self).__init__(NodeSearch(pending_id),
                                                 Login(ticket, response, user_cookie_name, detail_url))
        self.checked = False
        self.__to_commit = None


    def do_business(self):
        super(LoginCheckingEmail, self).do_business()
        pending_model = self[0].result
        main_user = self[1].result
        if _should_create_link(main_user, pending_model):
            self.checked = True
            self.__to_commit = ExternalToMainUser(origin=pending_model.external_user,
                                                  destination=pending_model.main_user)

    def commit(self):
        models = super(LoginCheckingEmail, self).commit()
        if self.__to_commit:
            models.append(self.__to_commit)
        return models




