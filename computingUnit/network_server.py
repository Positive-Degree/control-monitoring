#
# Created by Christophe Duchesne for Positive Degree
# 2018/08/06
#

import socket

port_number = 3196


def main():
    s = socket.socket()
    host = socket.gethostname()
    port = port_number
    s.bind((host, port))

    s.listen(5)  # Now wait for client connection.
    while True:
        c, client_address = s.accept()  # Establish connection with client.
        print('Got connection from', client_address)
        c.send('Thank you for connecting')
        c.close()


if __name__ == "__main__":
    main()
