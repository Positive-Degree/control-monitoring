#
# Created by Christophe Duchesne for Positive Degree
# 2018/08/06
#

import socket
import requests
import json
import os
import time
import pickle
from computingUnit.unit_control import ComputingUnit

# Unit listen port number
port_number = 31000
heroku_units_url = "https://positive-degree.herokuapp.com/units/"

# Json file name
unit_file_name = "unit_model"


# Network client associated with a unit to use networking functions
class UnitClient:

    def __init__(self, unit_json):
        self.unit = ComputingUnit(unit_json)

    # Sends HTTP GET with custom header to retrieve unit data from the central website DB
    def ping_for_update(self):
        # Custom http header to only request the unit's info as a json
        custom_headers = {'unit-update': "True"}
        response = requests.get(heroku_units_url + str(self.unit.id) + "/", headers=custom_headers)

        unit_values = response.json()[0]["fields"]
        self.unit.apply_changes(unit_values)


# Network server that receives frequent temperature updates from LAN Rpi
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
                temps = client_socket.recv(4096)
                print(pickle.loads(temps))
                # TODO : entry point of autonomous control depending of request
                client_socket.close()

        except KeyboardInterrupt:
            self.socket.close()


# Main script to run on each unit.
# - Pings the webserver frequently to stay updated with any changes made by a human controller
# - Runs a server instance to receive temperature updates from a local network connected Rpi for autonomous control
def main():

    # Each unit must have a local json model.
    # ** Valid path for windows only **
    path = str(os.path.dirname(os.path.abspath(__file__))) + "/" + unit_file_name
    with open(path, "r") as unit_file:
        unit = json.load(unit_file)
    unit_client = UnitClient(unit)

    while True:
        unit_client.ping_for_update()
        time.sleep(unit_client.unit.ping_frequency)


def local_networking_test():
    UnitServer()


if __name__ == "__main__":
    # main()
    local_networking_test()
