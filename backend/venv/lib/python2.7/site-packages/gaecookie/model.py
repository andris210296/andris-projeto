# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node


class SignSecret(Node):
    secret = ndb.StringProperty(required=True)

    @classmethod
    def find_last(cls):
        '''
        Returns the SignSecret ordered by desc creation
        '''
        return cls.query().order(-SignSecret.creation)
