"""Program to create the class to enable the connexion"""
import paramiko
class Connexion :
    """Class that enable the connexion"""

    def __init__(self,monitor):
        self.monitor=monitor
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.client.connect(hostname=self.monitor.hostname, username=self.monitor.username, password=self.monitor.password, port=self.monitor.port)  
    def get_client(self):
        """method to get client"""
        print(self.client)
        return self.client
