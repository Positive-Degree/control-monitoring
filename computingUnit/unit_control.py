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
from computingUnit.applications.gaming import GamingControl
from computingUnit.applications.mining import MiningControl

unit_json_model_path = str(os.path.dirname(os.path.abspath(__file__))) + "/unit_model"

# Unit fields names
unit_id_field = "unit_id"
unit_name_field = "name"
unit_ip_field = "ip_address"
unit_port_field = "port_number"
unit_process_field = "running_process"
unit_ping_field = "ping_frequency"

# Process values
mining_process = "mining"
gaming_process = "gaming"
webhosting_process = "webhosting"


# Represents a unit. Responsible for updating its local json model and triggering
# appropriate commands when changes happen
class ComputingUnit:
    def __init__(self, unit):
        self.id = unit[unit_id_field]
        self.name = unit[unit_name_field]
        self.ip_address = unit[unit_ip_field]
        self.port_number = unit[unit_port_field]
        self.running_process = unit[unit_process_field]
        self.ping_frequency = unit[unit_ping_field]

    def apply_changes(self, new_unit_values):

        has_changed = False

        # Attributes that trigger commands to be executed on unit
        if not new_unit_values[unit_process_field] == self.running_process:
            has_changed = True
            process_controller = UnitProcessControl(new_unit_values[unit_process_field])
            process_controller.change_process()

        # Basic unit infos
        if not new_unit_values[unit_name_field] == self.name or \
                not new_unit_values[unit_ip_field] == self.ip_address or \
                not new_unit_values[unit_port_field] == self.port_number or \
                not new_unit_values[unit_ping_field] == self.ping_frequency:
            has_changed = True

        if has_changed:
            self.update(new_unit_values)
            self.update_json_model(unit_json_model_path)

    # Update of the object unit values
    def update(self, new_unit_values):
        self.name = new_unit_values[unit_name_field]
        self.running_process = new_unit_values[unit_process_field]
        self.ip_address = new_unit_values[unit_ip_field]
        self.port_number = new_unit_values[unit_port_field]
        self.ping_frequency = new_unit_values[unit_ping_field]

    # Updates the local unit model json file
    def update_json_model(self, json_file_path):

        with open(json_file_path, "r") as unit_file:
            unit = json.load(unit_file)
        unit_file.close()

        unit[unit_name_field] = self.name
        unit[unit_port_field] = self.port_number
        unit[unit_ip_field] = self.ip_address
        unit[unit_process_field] = self.running_process
        unit[unit_ping_field] = self.ping_frequency

        with open(json_file_path, "w") as unit_file:
            json.dump(unit, unit_file)
        unit_file.close()


# Controls the processes or applications running on the machine
class UnitProcessControl:

    def __init__(self, new_process):
        self.commands = []
        self.new_process = new_process
        self.gaming_controller = GamingControl()
        self.mining_controller = MiningControl()

    def change_process(self):

        if self.new_process == mining_process:

            # Stop other processes
            command = commands.StopGaming(self.gaming_controller)
            self.store_command(command)

            # Start mining - applyging command pattern
            command = commands.StartMining(self.mining_controller)
            self.store_command(command)

        elif self.new_process == gaming_process:

            # Stop other processes
            command = commands.StopMining(self.mining_controller)
            self.store_command(command)

            # Applying command pattern
            command = commands.StartLeague(self.gaming_controller)
            self.store_command(command)

        elif self.new_process == webhosting_process:
            pass

        self.execute_commands()

    # Store a command for further execution
    def store_command(self, command):
        self.commands.append(command)

    # Executes all stored commands on different threads
    def execute_commands(self):
        for command in self.commands:
            command_thread = CommandThread(command)
            command_thread.start()


# Executes a single command on a thread
class CommandThread(Thread):
    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        self.command.execute()


# Sends new processes to process control depending on sensor temperature input
class TemperatureAnalyser(Thread):
    def __init__(self, temperatures):
        super().__init__()
        self.current_temperatures = temperatures


# For testing purposes
def main():
    pass


if __name__ == "__main__":
    main()
