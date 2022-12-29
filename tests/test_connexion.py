import unittest

import paramiko.ssh_exception

from models.Connexion import Connexion
from models.ConfigurationLoader import Config
class Test(unittest.TestCase):

    # Call before each test
    def setUp(self):
        self.configurations = Config()
        self.monitorTest = self.configurations.loadMachineConfiguration(0)

    def test_createClient(self):
        try:
            Connexion(self.monitorTest)
        except paramiko.ssh_exception.SSHException:
            self.fail("Exception raise")

if __name__ == '__main__':
    unittest.main()
