import unittest
from models.class_ApacheServerLogParser import LogParser
class Test(unittest.TestCase):

    def test_getLogLineData(self):
        apacheLogLine = LogParser('localhost:80 127.0.0.1 - - [06/Dec/2022:13:05:01 +0000] "GET /wp-cron.php HTTP/1.1" 200 131 "-" "Mozilla/5.0\"')
        self.assertEqual(apacheLogLine.getLogLineData()["remote_host"],'localhost:80')
        self.assertEqual(apacheLogLine.getLogLineData()["request_method"],'GET')
        self.assertEqual(apacheLogLine.getLogLineData()["remote_ip"],'127.0.0.1')
        self.assertEqual(apacheLogLine.getLogLineData()["status"],'200')
        self.assertEqual(apacheLogLine.getLogLineData()["request_url"],'/wp-cron.php')