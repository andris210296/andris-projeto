# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json

from webapp2_extras import securecookie

from gaecookie.manager import FindOrCreateSecrets


class SignCmd(FindOrCreateSecrets):
    def __init__(self, name, dct):
        self.name = name
        self.dct = dct
        self._find_secret = ()
        super(SignCmd, self).__init__()

    def do_business(self, stop_on_error=False):
        super(SignCmd, self).do_business(stop_on_error)
        secret = self.result
        if secret:
            value = json.dumps(self.dct)
            serializer = securecookie.SecureCookieSerializer(str(secret[0]))
            self.result = serializer.serialize(self.name, value)
        else:
            self.result = None


class RetrieveCmd(FindOrCreateSecrets):
    def __init__(self, name, signed, max_age):
        self.max_age = max_age
        self.name = name
        self.signed = signed
        super(RetrieveCmd, self).__init__()

    def do_business(self, stop_on_error=False):
        super(RetrieveCmd, self).do_business(stop_on_error)
        secrets = self.result
        if secrets:
            for s in secrets:
                serializer = securecookie.SecureCookieSerializer(str(s))
                data = serializer.deserialize(self.name, self.signed, self.max_age)
                if data:
                    self.result = json.loads(data)
                    return
        self.result = None
