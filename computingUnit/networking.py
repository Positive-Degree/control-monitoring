#
# Created by Christophe Duchesne for Positive Degree
# 2018/08/06
#

import socket
import requests
from threading import Thread
import json
import os
import time
import pickle
from computingUnit.unit_control import ComputingUnit, TemperatureAnalyser

# Unit listen port number
port_number = 31000
heroku_units_url = "https://positive-degree.herokuapp.com/units/"

# Json file name
unit_file_name = "unit_model"

manual_control_mode = "manual"
autonomous_control_mode = "autonomous"


# Network client associated with a unit to use networking functions
class UnitClient:

    def __init__(self, unit):
        self.unit = unit

    # Sends HTTP GET with custom header to retrieve unit data from the central website DB
    def ping_for_update(self):
        # Custom http header to only request the unit's info as a json
        custom_headers = {'unit-update': "True"}
        response = requests.get(heroku_units_url + str(self.unit.id) + "/", headers=custom_headers)
        unit_values = response.json()[0]["fields"]
        self.unit.apply_changes(unit_values)


# Network server that receives frequent temperature updates from LAN Rpi
class UnitServer:

    def __init__(self, unit):
        self.unit = unit
        self.socket = socket.socket()
        self.port = port_number
        self.setup_server()
        self.listen_incoming_connections()

    def setup_server(self):
        self.socket.bind(('', self.port))

    # Listens and accepts incoming client connections
    def listen_incoming_connections(self):
        try:
            self.socket.listen(5)  # Now wait for client connection.
            while True:
                client_socket, client_address = self.socket.accept()  # Establish connection with client.
                temps = client_socket.recv(4096)

                # Update unit instance when a connection is received
                self.unit.update_from_json()

                # Delegates temperatures to be analysed and trigger appropriate actions if
                # control mode is on autonomous
                if self.unit.control_mode == autonomous_control_mode:
                    analyser = TemperatureAnalyser(pickle.loads(temps), self.unit)
                    analyser.analyze_temperatures()

                client_socket.close()

        except KeyboardInterrupt:
            self.socket.close()

    def update_unit(self):
        pass


# Thread responsible for the client side
class ClientThread(Thread):
    def __init__(self, unit_client):
        super().__init__()
        self.unit_client = unit_client

    def run(self):
        while True:
            self.unit_client.ping_for_update()
            time.sleep(self.unit_client.unit.ping_frequency)


# Thread responsible for the server side
class ServerThread(Thread):
    def __init__(self, unit):
        super().__init__()
        self.unit = unit

    def run(self):
        UnitServer(self.unit)


# Main script that runs on each unit.
# - Pings the webserver frequently to stay updated with any changes made by a human controller (client part)
# - Receive temperature updates from a local network connected Rpi for autonomous control (server part)
def main():
    # Each unit must have a local json model file
    # ** Valid path for windows only **
    path = str(os.path.dirname(os.path.abspath(__file__))) + "\\" + unit_file_name
    with open(path, "r") as unit_file:
        unit_json = json.load(unit_file)

    unit = ComputingUnit(unit_json)
    unit_client = UnitClient(unit)

    client = ClientThread(unit_client)
    server = ServerThread(unit)

    client.start()
    server.start()


def test():
    path = str(os.path.dirname(os.path.abspath(__file__))) + "/" + unit_file_name
    with open(path, "r") as unit_file:
        unit_json = json.load(unit_file)

    unit = ComputingUnit(unit_json)
    unit_client = UnitClient(unit)

    unit_client.ping_for_update()


if __name__ == "__main__":
    # main()
    test()
