import paramiko

class Connexion :

    def __init__(self,monitor):
        self.monitor=monitor
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.client.connect(hostname=self.monitor.hostname, username=self.monitor.username, password=self.monitor.password, port=self.monitor.port)
        
    def getClient():
        return self.client
