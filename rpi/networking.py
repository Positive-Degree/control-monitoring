#
# Created by Christophe Duchesne for Positive Degree
# 2018/08/06
#

import socket
import requests

port_number = 31000
computing_unit_address = "127.0.0.1"
heroku_units_url = "https://positive-degree.herokuapp.com/units/"

# Unit fields names
unit_ip_field = "ip_address"
unit_port_field = "port_number"


# Network client who sends temperatures to local computing unit
class RpiUnitClient:

    def __init__(self, unit_id, unit_ip, unit_port_number):
        self.socket = socket.socket()
        self.unit_id = unit_id
        self.unit_ip = unit_ip
        self.unit_port_number = unit_port_number
        self.look_for_update()

    def _connect_to_unit(self):
        self.socket.connect((self.unit_ip, self.unit_port_number))

    def send_to_unit(self, message):
        self._connect_to_unit()
        self.socket.send(message)
        self.socket.close()

    # As in the computing unit, fetches data on the website DB to stay updated
    def look_for_update(self):
        custom_headers = {'unit-update': "True"}
        response = requests.get(heroku_units_url + str(self.unit_id) + "/", headers=custom_headers)

        # Updates unit connection info
        unit_values = response.json()[0]["fields"]
        self.unit_ip = str(unit_values[unit_ip_field])
        self.unit_port_number = unit_values[unit_port_field]


# For testing client individually
def main():
    client = RpiUnitClient(2, computing_unit_address, port_number)


if __name__ == "__main__":
    main()
