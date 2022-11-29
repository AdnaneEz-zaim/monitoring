import paramiko

class Connexion :

    def __init__(self,monitor):
       self.monitor=monitor

    
    def connect():
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        client.connect(hostname=monitor0.get_hostnames, username=monitor0.get_usernames, password=monitor0.get_passwords, port=monitor0.get_ports)
        return client

    # getter method
    def get_hostnames(self):
        return self.hostnames
    def get_usernames(self):
        return self.usernames
    def get_passwords(self):
        return self.passwords
    def get_ports(self):
        return self.ports