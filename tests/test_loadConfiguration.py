""" Fichier test loadConfiguration"""
import unittest
from models.class_config import Config

class Test(unittest.TestCase):
    """ Class test configuration loaded """

    # Call before each test
    def setUp(self):
        self.configurations = Config()
        self.monitor_test = self.configurations.loadMachineConfiguration(0)

    def test_constructor(self):
        """method to test constructor method"""
        self.assertTrue(self.monitor_test)

    def test_get_hostname(self):
        """method to test get_hostname method  """
        self.assertEqual(self.monitor_test[0], "leodagan.telecomste.net")

    def test_get_username(self):
        """method to test get_username method"""
        self.assertEqual(self.monitor_test[1], "grudu")

    def test_get_password(self):
        """method to test get_password method"""
        self.assertEqual(self.monitor_test[2], "113-TgBT-3784")

    def test_get_port(self):
        """method to test get_port method"""
        self.assertEqual(self.monitor_test[3], "22113")

if __name__ == '__main__':
    unittest.main()
