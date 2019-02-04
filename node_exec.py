#!/usr/bin/env python
"""
This module provide the inteface to execute command in local and remote hosts
"""

import paramiko
from sys import exit as sys_exit
from subprocess import Popen, Pipe
from collections import Mapping

class Node(object):
    """ Father class """
    def __init__(self, config=None):
        """ Initialize """
        self.hostname = config.get("hostname")

    def run_cmd(self, cmd=None):
        """ Section to run a command """
        pass


    def close(self):
        """ Close Connection """
        print "Nothing to do !"


class LocalNode(Node):
    """ Class to define Local Node behavior """
    def __init__(self, config=None):
        """ Initialize Local Node Object """
        super(LocalNode, self).__init__(config)
        self.localhost = True

    def run_cmd(self, cmd=None):
        """ Section to run a command """
        # Pyhton 2.X DO NOT support timeout
        proc = Popen(cmd, stdout=Pipe, stderr=Pipe, shell=True)
        out, err = proc.communicate()
        return proc.returncode, out, err


class RemoteNode(Node):
    """ Class to define Remote Node behavior """
    def __init__(self, config=None):
        """ Initialize Remote Node Object """
        super(RemoteNode, self).__init__(config)
        self.localhost = False
        self.user = config.get("username")
        self.password = config.get("password")

        if config.get("port") is not None:
            self.port = config["port"]
        else:
            self.port = 22
        # Set key and timeout if available
        self.ssh = None
        self.create_new_connection()


    def create_new_connection(self):
        """ Method to create a new Paramiko connection """
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        err = None
        try:
            self.ssh.connect(hostname = self.hostname,
                             port = self.port,
                             username = self.username,
                             password = self.password)
        except BadHostKeyException as err:
            print "[ERROR] BadHostKeyException has happened"
        except AuthenticationException as err:
            print "[ERROR] AuthenticationException has happened"
        except SSHException as err:
            print "[ERROR] SSHException has happened"
        except socket.error as err:
            print "[ERROR] socket.error has happened"
        finally:
            if err is not None:
                print "Error details: " + str(err)
                raise err
            print "Connection succeded !"


    def run_cmd(self, cmd=None, timeout=None):
        """ Section to run a command """
        _, stdout, stderr = self.ssh.exec_command(command = cmd,
                                                timeout = timeout)
        err = stderr.read()
        out = stdout.read()
        ret = stdout.channel.recv_exit_status()    
        return ret, out, err


    def close(self):
        """ Closing the paramiko connection """
        self.ssh.close()



def get_node(config=None):
    """ Return a Local or a Remote node object """
    if config.get("localhost") is True:
        return LocalNode(config)
    return RemoteNode(config)



if __name__ == "__main__":
    print "This is a module to import, not execute"
    sys_exit(1)
