#
# Created by Christophe Duchesne for Positive Degree
# 2018/08/03
#
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


# Empty concreteCommand template
class ConcreteCommand(Command):
    """
    Define a binding between a Receiver object and an action.
    Implement Execute by invoking the corresponding operation(s) on
    Receiver.
    """

    def execute(self):
        self._receiver.action()


class StartMining(Command):

    def execute(self):
        self._receiver.btc_mining()


class StartGaming(Command):

    def execute(self):
        self._receiver.steam_remote_gaming()


# Receiver class template for the command pattern.
class CommandReceiver:
    pass
