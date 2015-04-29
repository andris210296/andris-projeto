# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb


class CommandExecutionException(Exception):
    """
    Exception that indicates problems on execution
    """
    pass


def to_model_list(models):
    if models is None:
        return []
    return [models] if isinstance(models, ndb.Model) else models


class Command(object):
    def __init__(self):
        self.errors = {}
        self.result = None
        self._to_commit = None

    def update_errors(self, **errors):
        return self.errors.update(errors)


    def add_error(self, key, msg):
        self.errors[key] = msg

    def set_up(self):
        """
        Must set_up data for business.
        It should fetch data asyncrounously if needed
        """
        pass

    def do_business(self):
        """
        Must do the main business of use case
        """
        pass

    def commit(self):
        """
        Must return a Model, or a list of it to be committed on DB
        """
        if not self.errors:
            return self._to_commit

    def handle_previous(self, command):
        """
        Method called when commands are executed in sequence or parallel, so next command can access the previous
        just before executing do_business method. Override it if you need previous data
        :param command: previous command
        :return: None
        """
        pass

    def execute(self):
        self.set_up()
        self.do_business()
        if self.errors:
            raise CommandExecutionException(unicode(self.errors))
        ndb.put_multi(to_model_list(self.commit()))
        return self

    def __call__(self):
        self.execute()
        return self.result


class CommandListBase(Command):
    def __init__(self, *commands):
        super(CommandListBase, self).__init__()
        self.__commands = list(commands)

    def __getitem__(self, index):
        return self.__commands[index]

    def __len__(self):
        return len(self.__commands)

    def __nonzero__(self):
        return bool(self.__commands)

    def append(self, cmd):
        self.__commands.append(cmd)

    def extend(self, cmds):
        self.__commands.extend(cmds)


    def raise_exception_if_errors(self):
        if self.errors:
            raise CommandExecutionException(unicode(self.errors))


class CommandParallel(CommandListBase):
    def set_up(self):
        for cmd in self:
            cmd.set_up()

    def do_business(self):
        for cmd in self:
            try:
                cmd.do_business()
            except CommandExecutionException:
                pass
            self.update_errors(**cmd.errors)
        self.raise_exception_if_errors()
        if self:
            self.result = self[-1].result

    def commit(self):
        models = to_model_list(super(CommandParallel, self).commit())
        for cmd in self:
            models.extend(to_model_list(cmd.commit()))
        return models

    def handle_previous(self, command):
        [cmd.handle_previous(command) for cmd in self]


class CommandSequential(CommandListBase):
    def do_business(self):
        previous_cmd = None
        for cmd in self:
            if previous_cmd is not None:
                cmd.handle_previous(previous_cmd)
            try:
                cmd()
            except CommandExecutionException, e:
                self.update_errors(**cmd.errors)
                raise e
            previous_cmd = cmd
        if self:
            self.result = self[-1].result

    def handle_previous(self, command):
        self[0].handle_previous(command)
