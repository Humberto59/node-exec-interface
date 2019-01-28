#!/usr/bin/env python
"""
This module provide the inteface to execute command in local and remote hosts
"""

from sys import exit as sys_exit
from subprocess import Popen
from collections import Mapping

class Node(object):
    """ Father class """
    def __init__(self, config=None):
        """ Initialize """
        self.hostname = config.get("hostname")

    def run_cmd(self, cmd=None):
        """ Section to run a command """
        pass


class LocalNode(Node):
    """ Class to define Local Node behavior """
    def __init__(self, config=None):
        self.localhost = True

    def run_cmd(self, cmd=None):
        """ Section to run a command """
        Popen(cmd)
        pass


class RemoteNode(Node):
    """ Class to define Remote Node behavior """
    def __init__(self, config=None):
        self.localhost = False
        # Paramiko init

    def run_cmd(self, cmd=None):
        """ Section to run a command """
        #Paramiko exec
        pass


def get_node(config=None):
    """ Return a Local or a Remote node object """
    if config.get("localhost") is True:
        return LocalNode(config)
    return RemoteNode(config)



if __name__ == "__main__":
    print "This is a module to import, not execute"
    sys_exit(1)
