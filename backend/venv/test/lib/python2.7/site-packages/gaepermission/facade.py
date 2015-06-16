# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import Command
from gaebusiness.gaeutil import ModelSearchCommand
from gaecookie import facade as cookie_facade
from gaegraph.business_base import NodeSearch
from gaepermission import inspector
from gaepermission.base_commands import UpdateUserGroups, GetMainUserByEmail, SaveUserCmd
from gaepermission.base_commands2 import LoginCheckingEmail
from gaepermission.facebook.commands import GetFacebookApp, SaveOrUpdateFacebookApp, LogFacebookUserIn, FetchFacebook
from gaepermission.google.commands import GoogleLogin
from gaepermission.model import MainUser
from gaepermission.passwordless.commands import SaveOrUpdateApp, GetApp, SengLoginEmail, Login
from tekton import router

USER_COOKIE_NAME = 'userck'


def save_user_cmd(email, name=None, groups=None, locale='en_US', timezone='US/Eastern'):
    """
    Command to save a user
    :param email: user email
    :param name: user name
    :param groups: user permission groups
    :return: A command that validate date and save the user
    """
    if name is None:
        name = email
    if groups is None:
        groups = []
    return SaveUserCmd(name=name, email=email, groups=groups, locale=locale, timezone=timezone)


def get_user_by_email(email):
    """
    Returns a command that find MainUser by her email address
    :param email: email to use in search
    :return: Command that look for user on DB
    """
    return GetMainUserByEmail(email)


def web_path_security_info():
    """
    Returns a generator that returns all paths from the application if information about groups and csrf security
    """
    return inspector.web_paths_security_info(router.package_base)


def logout(response):
    """
    Returns a command that log the user out, removing her id from cookie
    """
    return cookie_facade.delete_cookie(response, USER_COOKIE_NAME)


def logged_user(request):
    """
    Returns a command that retrieves the current logged user based on secure cookie
    If there is no logged user, the result from command is None
    """
    dct = cookie_facade.retrive_cookie_data(request, USER_COOKIE_NAME).execute().result
    if dct is None:
        return Command()
    return NodeSearch(dct['id'])


def login_google(google_user, response):
    """
    Google user must be the user returned from get_current_user from users module provided by App Engine
    Returns a command that log user in based on her google account credentials.
    The logged user (MainUser) is provides on result or None if the user is not logged with her Google Account
    """

    return GoogleLogin(google_user, response, USER_COOKIE_NAME)


def login_passwordless(ticket, response, detail_url='https://pswdless.appspot.com/rest/detail'):
    """
    Log user in using Passwordless service
    :param ticket: ticket returned from Passwordless
    :param response: Response object from webapp2
    :param detail_url: url to check ticket and user data
    :return: a Command that log user in when executed
    """
    return Login(ticket, response, USER_COOKIE_NAME, detail_url)


def login_checking_email(pending_id, ticket, response, detail_url='https://pswdless.appspot.com/rest/detail'):
    """
    Log user in using Passwordless service
    :param pending_id: PendingExternalToMainUser's id
    :param ticket: ticket returned from Passwordless
    :param response: Response object from webapp2
    :param detail_url: url to check ticket and user data
    :return: a Command that log user in when executed
    """
    return LoginCheckingEmail(pending_id, ticket, response, USER_COOKIE_NAME, detail_url)


def update_user_groups(user_id, groups):
    """
    Returns a command that updates user's groups of respective user_id.
    """
    return UpdateUserGroups(user_id, groups)


def find_users_by_email_starting_with(email_prefix=None, cursor=None, page_size=30):
    """
    Returns a command that retrieves users by its email_prefix, ordered by email.
    It returns a max number of users defined by page_size arg. Next result can be retrieved using cursor, in
    a next call. It is provided in cursor attribute from command.
    """
    email_prefix = email_prefix or ''

    return ModelSearchCommand(MainUser.query_email_starts_with(email_prefix),
                              page_size, cursor, cache_begin=None)


def find_users_by_email_and_group(email_prefix=None, group=None, cursor=None, page_size=30):
    """
    Returns a command that retrieves users by its email_prefix, ordered by email and by Group.
    If Group is None, only users without any group are going to be searched
    It returns a max number of users defined by page_size arg. Next result can be retrieved using cursor, in
    a next call. It is provided in cursor attribute from command.
    """
    email_prefix = email_prefix or ''

    return ModelSearchCommand(MainUser.query_email_and_group(email_prefix, group),
                              page_size, cursor, cache_begin=None)



def send_passwordless_login_link(email, return_url, lang='en_US', url_login='https://pswdless.appspot.com/rest/login'):
    """

    :param app_id: The Passwordless app's id
    :param token: The Passwordless app's token
    :param return_url: The url user will be redirected after clicking login link
    :return: command that communicate with passsworless to sent the email
    """
    return SengLoginEmail(email, return_url, lang, url_login)


def save_or_update_passwordless_app_data(id=None, token=None):
    """
    :param id: The App's id
    :param token: The App's token
    :return: a command that save or update existing Passwordless App Data
    See https://pswdless.appspot.com/api#register-sites
    """
    return SaveOrUpdateApp(id, token)


def get_passwordless_app_data():
    """
    :return: a command that returns the Passwordless App Data from db
    """
    return GetApp()


def get_facebook_app_data():
    """
    :return: a command that returns the Facebook App Data from db
    """
    return GetFacebookApp()


def save_or_update_facebook_app_data(id=None, token=None):
    """
    :param id: The App's id
    :param token: The App's token
    :return: a command that save or update existing Facebook App Data
    See https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow/v2.0
    """
    return SaveOrUpdateFacebookApp(id, token)



def login_facebook(token, response):
    """

    :param token: facebook request token
    :param response: http response from webapp2
    :return: a command that log the facebook user in
    """
    return LogFacebookUserIn(token, response, USER_COOKIE_NAME)
