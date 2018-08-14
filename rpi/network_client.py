#
# Created by Christophe Duchesne for Positive Degree
# 2018/08/06
#

import socket
import time
import requests
import json

port_number = "8080"
laptop_public_host_url = "https://positive-degree.herokuapp.com/units/1/"


def main():

    custom_headers = {'unit-update': "True"}
    response = requests.get(laptop_public_host_url, headers=custom_headers)
    print(response.json()[0]["fields"]["running_process"])


if __name__ == "__main__":
    main()
