"""Program to create the class to enable the connexion"""
import paramiko
class Connexion :
    """Class that enable the connexion"""

    def __init__(self,monitor):
        
        try:
            self.monitor=monitor
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            self.client.connect(hostname=self.monitor[0], username=self.monitor[1], password=self.monitor[2], port=self.monitor[3])
        except (paramiko.ssh_exception.SSHException) as e:
            print('ERROR', ('A connection to the server could not be established '))

                
        
    def get_client(self):
        """method to get client"""
        print(self.client)
        return self.client
