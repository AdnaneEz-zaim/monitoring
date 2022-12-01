import unittest
from models.class_config import Config


class Test(unittest.TestCase):

    # Call before each test
    def setUp(self):
       self.monitorTest = Config(0)

    def test_constructor(self):
        self.assertTrue(self.monitorTest)

    def test_getHostname(self):
        self.assertEqual(self.monitorTest.get_hostname(), "leodagan.telecomste.net")

    def test_getUsername(self):
        self.assertEqual(self.monitorTest.get_username(), "grudu")

    def test_getPassword(self):
        self.assertEqual(self.monitorTest.get_password(), "113-TgBT-3784")

    def test_getPort(self):
        monitorTest = Config(0)
        self.assertEqual(self.monitorTest.get_port(), "22113")


if __name__ == '__main__':
    unittest.main()
