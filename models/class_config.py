"""Program for the config class """
import configparser
import os.path

class Config:
    """Class to define the config of the machines"""
    def __init__(self, id):
        # CONFIGURATION FILE PATH
        absolute_path = os.path.dirname(__file__)
        relative_path = "../config.ini"
        path_config_file = os.path.join(absolute_path,relative_path)

        # Loading configuration file ----------------------------------------
        config = configparser.ConfigParser()
        config.read(path_config_file)

        machines_hostnames = config['monitored_machines']['hostnames'].split(';')
        machines_usernames = config['monitored_machines']['usernames'].split(';')
        machines_passwords = config['monitored_machines']['passwords'].split(';')
        machines_ports = config['monitored_machines']['ports'].split(';')

        print("-----------------[Machine" + str(id) + "]-----------------")
        print(machines_hostnames[id])
        print(machines_usernames[id])
        print(machines_passwords[id])
        print(machines_ports[id])

        print("Machine" + str(id) + " configuration successfully loaded !")
        print("--------------------------------------------")

        # Init attributes
        self.hostname = machines_hostnames[id]
        self.username = machines_usernames[id]
        self.password = machines_passwords[id]
        self.port = machines_ports[id]

    # getter method
    def get_hostname(self):
        """method to get the hostname"""
        return self.hostname

    def get_username(self):
        """method to get username"""
        return self.username

    def get_password(self):
        """method to get password"""
        return self.password

    def get_port(self):
        """method to get port"""
        return self.port
