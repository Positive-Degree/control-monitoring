#
# Created by Christophe Duchesne for Positive Degree
# 2018/08/06
#

import socket
import requests
import json
import os
import time
from computingUnit.unit_control import ComputingUnit
from computingUnit.unit_control import UnitControlThread

# Unit listen port number
port_number = 2000
heroku_units_url = "https://positive-degree.herokuapp.com/units/"


# The network client associated with a unit to keep it updated
class UnitClient:

    def __init__(self, unit_json):
        self.unit = ComputingUnit(unit_json)

    # Sends HTTP GET with custom header to retrieve unit data from the central website DB
    def ping_for_update(self):
        custom_headers = {'unit-update': "True"}
        response = requests.get(heroku_units_url + str(self.unit.id) + "/", headers=custom_headers)
        unit_values = response.json()[0]["fields"]
        self.unit.apply_changes(unit_values)


class UnitServer:

    def __init__(self):
        self.socket = socket.socket()
        self.port = port_number
        self.setup_server()
        self.listen_incoming_connections()

    def setup_server(self):
        self.socket.bind(('', self.port))

    def listen_incoming_connections(self):
        try:
            self.socket.listen(5)  # Now wait for client connection.
            while True:
                client_socket, client_address = self.socket.accept()  # Establish connection with client.

                control_thread = UnitControlThread(client_socket)
                control_thread.run()
                client_socket.close()

        except KeyboardInterrupt:
            self.socket.close()


def socket_exit_handler(socket_to_close):
    socket_to_close.close()
    print("Socket closed.")


def main():

    path = str(os.path.dirname(os.path.abspath(__file__))) + "/unit_model"
    with open(path, "r") as unit_file:
        unit = json.load(unit_file)
    unit_client = UnitClient(unit)
    unit_client.ping_for_update()

    # while True:
    #     unit_client.ping_for_update()
    #     time.sleep(unit_client.unit.ping_frequency)


if __name__ == "__main__":
    main()
