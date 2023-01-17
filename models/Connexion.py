"""Program to create the class to enable the connexion"""
import paramiko


class Connexion:
    """Class that enable the connexion"""

    def __init__(self, monitor):
        self.monitor = monitor
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.client.connect(hostname=self.monitor[0],
                            username=self.monitor[1],
                            password=self.monitor[2],
                            port=self.monitor[3])

    def get_client(self):
        """getter client"""
        return self.client
