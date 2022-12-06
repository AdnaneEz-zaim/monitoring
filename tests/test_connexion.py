import unittest
from models.class_connexion import Connexion
from models.class_config import Config
class Test(unittest.TestCase):

    # Call before each test
    def setUp(self):
       self.monitorTest = Config(0)

    def test_createClient(self): # doesnt work because it return an object even if bad credential connexion
        self.assertTrue(Connexion(self.monitorTest).getClient())

if __name__ == '__main__':
    unittest.main()
