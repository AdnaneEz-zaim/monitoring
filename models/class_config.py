import configparser


class Config:

    def __init__(self, id):
        # CONFIGURATION FILE PATH
        path_configFile = "config.ini"

        # Loading configuration file ----------------------------------------
        config = configparser.ConfigParser()
        config.read(path_configFile)

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
        return self.hostname

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_port(self):
        return self.port
