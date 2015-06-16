# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.manager import RenewSecrets, RevokeSecrets
from gaecookie.cookie import DeleteCookie, WriteCookie, RetrieveCookieData
from gaecookie.security import SignCmd, RetrieveCmd


def retrive_cookie_data(request, cookie_name):
    '''
    Returns a command that retrieves a obj from signed json encoded string on cookie
    '''
    return RetrieveCookieData(request, cookie_name)


def delete_cookie(response, cookie_name):
    '''
    Returns a command that erase
    '''
    return DeleteCookie(response, cookie_name)


def write_cookie(response, cookie_name, obj):
    '''
    Returns a command that write obj on cookie as a signed json encoded string
    '''
    return WriteCookie(response, cookie_name, obj)


def sign(name, obj):
    '''
    Returns a command that encode obj as a signed json string
    '''
    return SignCmd(name, obj)


def retrieve(name, signed, max_age=604800):
    '''
    Returns the obj on result contained on the signed json string coded if it is valid.
     The content can be invalid by someone trying to fake it or because it is above max age.
     max_age in seconds. Default seven days
    '''
    return RetrieveCmd(name, signed, max_age)


def renew():
    '''
    Returns a command that when executed, renews the secret.
    By secret renewing, the security is improved. A cron can be used to renew it with frequency.
    The last secret will be still valid, but the new one will be used to sign new itens.
    Once the sign has expire date, the old secret will be changed to new one gradually
    '''
    return RenewSecrets()


def revoke():
    '''
    Returns a command that when executed, revoke the secrets and create new ones.
    Works like renew, but it invalidates the last secret so content signed with it are not allowed
    Use this when the secret is compromised
    '''
    return RevokeSecrets()
