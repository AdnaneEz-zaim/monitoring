"""Test of ApacheServerLogParser """

import unittest
from models.ApacheServerLogParser import LogParser
class Test(unittest.TestCase):
    """Class to test methods from ApacheServerLogParser class"""
    def test_get_log_line_data(self):
        """method test the get_log_line_data method"""
        apache_log_line = LogParser('localhost:80 127.0.0.1 - - [06/Dec/2022:13:05:01 +0000] "GET /wp-cron.php HTTP/1.1" 200 131 "-" "Mozilla/5.0\"')
        self.assertEqual(apache_log_line.get_log_line_data()["remote_host"],'localhost:80')
        self.assertEqual(apache_log_line.get_log_line_data()["request_method"],'GET')
        self.assertEqual(apache_log_line.get_log_line_data()["remote_ip"],'127.0.0.1')
        self.assertEqual(apache_log_line.get_log_line_data()["status"],'200')
        self.assertEqual(apache_log_line.get_log_line_data()["request_url"],'/wp-cron.php')
        