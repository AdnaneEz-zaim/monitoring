import unittest

import paramiko.ssh_exception

from models.class_connexion import Connexion
from models.class_config import Config
class Test(unittest.TestCase):

    # Call before each test
    def setUp(self):
       self.monitorTest = Config(0)

    def test_createClient(self):
        try:
            Connexion(self.monitorTest)
        except paramiko.ssh_exception.SSHException:
            self.fail("Exception raise")

if __name__ == '__main__':
    unittest.main()
