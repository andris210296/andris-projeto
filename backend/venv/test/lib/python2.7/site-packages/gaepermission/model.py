# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaeforms.ndb.property import Email
from gaegraph.model import Node, Arc

_USER_WITHOUT_GROUP = 'USER_WITHOUT_GROUP'


class MainUser(Node):
    name = ndb.StringProperty(required=True)
    email = Email(required=True)
    groups = ndb.StringProperty(repeated=True)
    locale = ndb.StringProperty(indexed=False)
    timezone = ndb.StringProperty(indexed=False)

    def _pre_put_hook(self):
        if not self.groups:
            self.groups = ['']
        else:
            self.groups = [g for g in self.groups if g]


    @classmethod
    def _calculate_prefix(cls, prefix):
        last_str_with_prefix = prefix + unichr(65525)  # this is the last unichar supported on windows systems
        return last_str_with_prefix

    @classmethod
    def query_email_starts_with(cls, prefix=''):
        last_str_with_prefix = cls._calculate_prefix(prefix)
        return cls.query(cls.email >= prefix, cls.email < last_str_with_prefix).order(cls.email)


    @classmethod
    def query_email_and_group(cls, prefix, group):
        last_str_with_prefix = cls._calculate_prefix(prefix)
        if group is None:
            group = ''
        return cls.query(cls.email >= prefix, cls.email < last_str_with_prefix, cls.groups == group).order(cls.email)


    @classmethod
    def query_email(cls, email):
        return cls.query(cls.email == email)


# Users from external providers

class ExternalUser(Node):
    external_id = ndb.StringProperty(required=True)

    @classmethod
    def query_by_external_id(cls, external_id):
        return cls.query(cls.external_id == external_id)


class PendingExternalToMainUser(Node):
    """
    Class used to create ExternalToMainUser after email confirmation
    """
    main_user = ndb.KeyProperty(MainUser, required=True, indexed=False)
    external_user = ndb.KeyProperty(required=True, indexed=False)
    # name = ndb.StringProperty(required=True, indexed=False)
    # email = ndb.StringProperty(required=True, indexed=False)


class GoogleUser(ExternalUser):
    pass


class PasswordlessUser(ExternalUser):
    pass


class FacebookUser(ExternalUser):
    pass

class ExternalToMainUser(Arc):
    destination = ndb.KeyProperty(MainUser, required=True)
    origin = ndb.KeyProperty(ExternalUser, required=True)



