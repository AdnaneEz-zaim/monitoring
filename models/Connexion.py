"""Program to create the class to enable the connexion"""
import paramiko


class Connexion:
    """Class that enable the connexion"""

    def __init__(self, monitor):
        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            self.client.connect(hostname=monitor.hostname,
                                username=monitor.username,
                                password=monitor.password,
                                port=monitor.port)
        except paramiko.ssh_exception.AuthenticationException as e:
            print(f"Authentication failed: {e}")
            self.client = None
        except paramiko.ssh_exception.SSHException as e:
            print(f"An SSH error occurred: {e}")
            self.client = None
        except Exception as e:
            print(f"An error occurred: {e}")
            self.client = None
