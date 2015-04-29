# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node


class PasswordlessApp(Node):
    '''
     Class that hold data from Passwordless
     See https://pswdless.appspot.com/api#register-sites
    '''
    app_id = ndb.StringProperty(required=True, indexed=False)
    token = ndb.StringProperty(required=True, indexed=False)

# class PasswordlessLoginToken(Node):
#     '''
#     Class to hold login sent token, so it is possible certify login calls
#     '''
#     token = ndb.StringProperty(required=True, indexed=False)
