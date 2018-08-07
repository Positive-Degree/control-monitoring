#
# Created by Christophe Duchesne for Positive Degree
# 2018/08/06
#

from rpi.temp_monitoring import TempSensor
import socket

port_number = 3196


def main():
    s = socket.socket()
    host = socket.gethostname()
    port = port_number

    s.connect((host, port))
    print(s.recv(1024))
    s.close()


if __name__ == "__main__":
    main()
