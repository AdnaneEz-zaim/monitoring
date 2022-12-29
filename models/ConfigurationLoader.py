"""Program for the config class """
import configparser
import os.path

class Config:
    """Class to define the config of the machines"""
    def __init__(self):
        # CONFIGURATION FILE PATH
        absolute_path = os.path.dirname(__file__)
        relative_path = "../config.ini"
        path_config_file = os.path.join(absolute_path, relative_path)

        # Loading configuration file ----------------------------------------
        config = configparser.ConfigParser()
        config.read(path_config_file)

        self.machines_hostnames = config['monitored_machines']['hostnames'].split(';')
        self.machines_usernames = config['monitored_machines']['usernames'].split(';')
        self.machines_passwords = config['monitored_machines']['passwords'].split(';')
        self.machines_ports = config['monitored_machines']['ports'].split(';')

        # Set the number of machine configurations
        self.nbMachineConfig = min(len(self.machines_hostnames),
                                   len(self.machines_usernames),
                                   len(self.machines_passwords),
                                   len(self.machines_ports))

        print("Loaded " + str(self.nbMachineConfig) + " machine configurations")

    # getter method
    def loadMachineConfiguration(self, id):
        """method that return all the authentication credential associated to the given id"""
        if id < self.nbMachineConfig:
            print("-----------------[Machine" + str(id) + "]-----------------")
            print(self.machines_hostnames[id])
            print(self.machines_usernames[id])
            print(self.machines_passwords[id])
            print(self.machines_ports[id])

            print("Machine" + str(id) + " configuration successfully loaded !")
            print("--------------------------------------------")

            # Return authentication credential
            return self.machines_hostnames[id], self.machines_usernames[id], self.machines_passwords[id], self.machines_ports[id]

    def getNbMachineConfigurations(self):
        """ return the number of machine configuration loaded from the config.ini file"""
        return self.nbMachineConfig

