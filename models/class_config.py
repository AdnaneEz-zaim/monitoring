class Config:

    def __init__(self,hostnames,usernames,passwords,ports):
        self.hostnames = hostnames
        self.usernames = usernames
        self.passwords = passwords
        self.ports = ports
        
    # getter method
    def get_hostnames(self):
        return self.hostnames
    def get_usernames(self):
        return self.usernames
    def get_passwords(self):
        return self.passwords
    def get_ports(self):
        return self.ports
