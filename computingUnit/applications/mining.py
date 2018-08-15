#
# Created by Christophe Duchesne for Positive Degree
# 2018/08/03
#
# Command pattern reference : https://sourcemaking.com/design_patterns/command/python/1
#
import socket
import json
from idna import unicode
import subprocess

cg_miner_exe_path = 'C:\cgminer\cgminer'
cg_miner_params = "-o stratum+tcp://stratum.antpool.com:3333 -u PositiveDegree.testunit "

command = "C:\cgminer\cgminer -o stratum+tcp://stratum.antpool.com:3333 -u PositiveDegree.testunit -p \"\" "
lol = 'C:\\Riot Games\\League of Legends\\LeagueClient'


class MiningControl:

    def __init__(self):
        self.cgminerapi = CgminerAPI()
        pass

    def stop_cgminer(self):
        try:
            self.cgminerapi.quit()
        except OSError:
            print("Mining was not running.")

    def start_cgminer(self):
        subprocess.call(command)
        pass


# Source : https://thomassileo.name/blog/2013/09/17/playing-with-python-and-cgminer-rpc-api/
# Used to send commands to the local cgminer via the API
class CgminerAPI(object):
    """ Cgminer RPC API wrapper. """

    def __init__(self, host='localhost', port=4028):
        self.data = {}
        self.host = host
        self.port = port

    def command(self, command, arg=None):
        """ Initialize a socket connection,
        send a command (a json encoded dict) and
        receive the response (and decode it).
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((self.host, self.port))
            payload = {"command": command}
            if arg is not None:
                # Parameter must be converted to basestring (no int)
                payload.update({'parameter': unicode(arg)})

            sock.send(json.dumps(payload).encode())
            received = self._receive(sock)
        finally:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()

        return json.loads(received[:-1])

    def _receive(self, sock, size=4096):
        msg = ''
        while 1:
            chunk = sock.recv(size)
            if chunk:
                msg += chunk.decode()
            else:
                break
        return msg

    def __getattr__(self, attr):
        def out(arg=None):
            return self.command(attr, arg)
        return out


# For testing purposes
def main():
    subprocess.call(lol)


if __name__ == "__main__":
    main()
