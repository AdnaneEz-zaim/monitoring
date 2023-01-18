"""Program for the config class """
import configparser
import os.path
from models.MonitorManager import Monitor


class Config:
    """Class to define the config of the machines"""

    def __init__(self):
        # CONFIGURATION FILE PATH
        self.monitors = []
        self.nbMachineConfig = 0

        # Get path config file
        absolute_path = os.path.dirname(__file__)
        relative_path = "../config.ini"
        self.path_config_file = os.path.join(absolute_path, relative_path)

        # Read file and set attributes
        self.readMachineConfiguration()

    def readMachineConfiguration(self):
        # Loading configuration file ----------------------------------------
        config = configparser.ConfigParser()
        if not os.path.exists(self.path_config_file):
            # Create configuration file
            print("NO CONFIGURATION FILE FOUND, GENERATING ONE ...")
            config['monitored_machines'] = {'hostnames': '', 'usernames': '', 'passwords': '', 'ports': ''}

            # Write the new values to the config file
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

            print("DEFAULT CONFIGURATION FILE CREATED")

        # Read
        config.read(self.path_config_file)

        # Set attributes not null
        machines_hostnames = [elem for elem in config['monitored_machines']['hostnames'].split(';') if elem != '']
        machines_usernames = [elem for elem in config['monitored_machines']['usernames'].split(';') if elem != '']
        machines_passwords = [elem for elem in config['monitored_machines']['passwords'].split(';') if elem != '']
        machines_ports = [elem for elem in config['monitored_machines']['ports'].split(';') if elem != '']

        # Set the number of machine configurations
        self.nbMachineConfig = min(len(machines_hostnames),
                                   len(machines_usernames),
                                   len(machines_passwords),
                                   len(machines_ports))

        print("Loaded " + str(self.nbMachineConfig) + " machine configurations")

        for mac in range(self.nbMachineConfig):
            self.monitors.append(Monitor(machines_hostnames[mac],
                                         machines_usernames[mac],
                                         machines_passwords[mac],
                                         machines_ports[mac]
                                         ))

    # getter method
    def getMachineConfiguration(self, machine_id):
        """method that return all the authentication credential associated to the given id"""
        if machine_id < self.nbMachineConfig:
            print("-----------------[Machine" + str(machine_id) + "]-----------------")
            print(self.monitors[machine_id].hostname)
            print(self.monitors[machine_id].username)
            print(self.monitors[machine_id].password)
            print(self.monitors[machine_id].port)
            print("--------------------------------------------")

            # Return the monitor
            return self.monitors[machine_id]

    def getNbMachineConfigurations(self):
        """ return the number of machine configuration loaded from the config.ini file"""
        return self.nbMachineConfig

    def setMachineConfiguration(self, newHostname, newUsername, newPassword, newPort):
        # Initialize config parser
        config = configparser.ConfigParser()
        # Read config file
        config.read('config.ini')

        # Add new monitors to the current list
        self.monitors.append(Monitor(newHostname, newUsername, newPassword, newPort))
        self.nbMachineConfig = len(self.monitors)

        # Create the new parameter line in the config file
        separator = ";"
        list_hostnames = []
        list_usernames = []
        list_passwords = []
        list_ports = []

        for machine_id in range(len(self.monitors)):
            list_hostnames.append(self.monitors[machine_id].hostname)
            list_usernames.append(self.monitors[machine_id].username)
            list_passwords.append(self.monitors[machine_id].password)
            list_ports.append(self.monitors[machine_id].port)

        hostnames = separator.join(list_hostnames)
        usernames = separator.join(list_usernames)
        passwords = separator.join(list_passwords)
        ports = separator.join(list_ports)

        # Set the new values of the parameters
        config.set('monitored_machines', 'hostnames', hostnames)
        config.set('monitored_machines', 'usernames', usernames)
        config.set('monitored_machines', 'passwords', passwords)
        config.set('monitored_machines', 'ports', ports)

        # Write the new values to the config file
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
