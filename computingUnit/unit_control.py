#
# Created by Christophe Duchesne for Positive Degree
# 2018/08/03
#
# Command pattern reference : https://sourcemaking.com/design_patterns/command/python/1
#

from threading import Thread
import os
import json
import computingUnit.commands as commands

unit_json_model_path = str(os.path.dirname(os.path.abspath(__file__))) + "/unit_model"


# Represents a unit. Responsible for updating its local json model and triggering
# appropriate commands when changes happen
class ComputingUnit:
    def __init__(self, unit):
        self.id = unit["unit_id"]
        self.name = unit["name"]
        self.ip_address = unit["ip_address"]
        self.port_number = unit["port_number"]
        self.running_process = unit["running_process"]
        self.ping_frequency = unit["ping_frequency"]

    def apply_changes(self, new_unit_values):

        # Attributes that trigger commands to be executed on unit
        if not new_unit_values["running_process"] == self.running_process:

            self.running_process = new_unit_values["running_process"]
            # TODO : entry point of command pattern - with UnitControlThread ?

        # Basic unit infos
        if not new_unit_values["name"] == self.name or \
                not new_unit_values["ip_address"] == self.ip_address or \
                not new_unit_values["port_number"] == self.port_number or \
                not new_unit_values["ping_frequency"] == self.ping_frequency:
            self.update(new_unit_values)

        self.update_json_model(unit_json_model_path)

    # Update of the object unit values
    def update(self, new_unit_values):
        self.name = new_unit_values["name"]
        self.ip_address = new_unit_values["ip_address"]
        self.port_number = new_unit_values["port_number"]
        self.ping_frequency = new_unit_values["ping_frequency"]

    def update_json_model(self, json_file_path):

        with open(json_file_path, "r") as unit_file:
            unit = json.load(unit_file)
        unit_file.close()

        unit["name"] = self.name
        unit["port_number"] = self.port_number
        unit["ip_address"] = self.ip_address
        unit["ping_frequency"] = self.ping_frequency

        with open(json_file_path, "w") as unit_file:
            json.dump(unit, unit_file)
        unit_file.close()


# Thread launched for each incoming unit_model.json control request
class UnitControlThread(Thread):

    def __init__(self, socket):
        super().__init__()
        self.commands = []
        self.client_socket = socket

    def run(self):
        client_msg = str(self.client_socket.recv(1024))
        print(client_msg)

        # TODO : to be replaced with messaging protocol
        if client_msg == "b'11'":
            response = "Process changed to crypto mining"

            # Applying command pattern
            # TODO : Command factory ?
            receiver = MiningControl()
            command = commands.StartMining(receiver)
            self.store_command(command)

        elif client_msg == "b'12'":
            response = "Process changed to gaming"

            # Applying command pattern
            # TODO : Command factory ?
            receiver = GamingControl()
            command = commands.StartGaming(receiver)
            self.store_command(command)

        elif client_msg == "b'13'":
            response = "Process changed to web hosting"
        else:
            response = "Connection established with unit_model.json but nothing changed"

        self.execute_commands()
        self.send_response(response)

    def store_command(self, command):
        self.commands.append(command)

    def execute_commands(self):
        for command in self.commands:
            command.execute()

    def send_response(self, response):
        self.client_socket.send(response.encode())


class MiningControl:

    def __init__(self):
        pass

    def btc_mining(self):
        self.setup_cg_miner()
        print("Mining started")

    def setup_cg_miner(self):
        pass


class GamingControl:

    def __init__(self):
        pass

    def steam_remote_gaming(self):
        print("Gaming started")


def main():
    pass
    # receiver = Receiver()
    # concrete_command = ConcreteCommand(receiver)
    # invoker = Invoker()
    # invoker.store_command(concrete_command)
    # invoker.execute_commands()


if __name__ == "__main__":
    main()
