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

# Paths variable for application launches.
# ** Valid for the first windows unit only **
cg_miner_exe_path = 'C:\cgminer\cgminer'
cgminer_conf_path = 'C:\cgminer\cgminer.conf'
kryptex_path = 'C:\\Users\\PositiveDegree\\AppData\\Local\\Kryptex\\Kryptex.exe'
nicehash_path = 'C:\\Users\\PositiveDegree\\AppData\\Local\\Programs\\NiceHash Miner 2\\NiceHash Miner 2.exe'

kryptex_kill = 'taskkill /im Kryptex.exe /F /t'
nicehash_kill = 'taskkill /im NiceHash Miner 2.exe /t'


class MiningControl:

    def __init__(self):
        self.cgminerapi = CgminerAPI()
        pass

    def stop_cgminer(self):
        try:
            self.cgminerapi.quit()
        except OSError:
            print("CGminer was not running.")

    def start_cgminer(self):
        subprocess.call([cg_miner_exe_path, "-c", cgminer_conf_path])

    def start_kryptex(self):
        subprocess.call(kryptex_path)

    def stop_kryptex(self):
        try:
            subprocess.call(kryptex_kill)
        except:
            print("Kryptex was not running.")

    def start_nicehash(self):
        subprocess.call(nicehash_path)

    def stop_nicehash(self):
        try:
            subprocess.call(nicehash_kill)
        except:
            print("NiceHash was not running")


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

        return json.loads(received)

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
    subprocess.call(kryptex_kill)


if __name__ == "__main__":
    main()
