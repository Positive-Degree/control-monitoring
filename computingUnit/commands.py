#
# Created by Christophe Duchesne for Positive Degree
# 2018/08/03
#
# Module used for the implementation of the command pattern.
# Command pattern reference : https://sourcemaking.com/design_patterns/command/python/1
#

import abc


# The command interface
class Command(metaclass=abc.ABCMeta):

    def __init__(self, receiver):
        self._receiver = receiver

    @abc.abstractmethod
    def execute(self):
        pass


# CONCRETE COMMANDS #


class StopMining(Command):

    def execute(self):
        self._receiver.stop_kryptex()


class StartMining(Command):

    def execute(self):
        self._receiver.start_kryptex()


class StartLeague(Command):

    def execute(self):
        self._receiver.start_LOL()


class StartGaming(Command):

    def execute(self):
        self._receiver.start_steam()


class StopGaming(Command):

    def execute(self):
        self._receiver.stop_steam()

