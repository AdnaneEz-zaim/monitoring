import unittest
from models.class_ApacheServerLogInfo import LogInfo
from models.class_ApacheServerLogParser import LogParser
class Test(unittest.TestCase):
    def setUp(self):
        self.list_data = [
            'localhost:80 127.0.0.1 - - [06/Dec/2022:14:00:01 +0000] "GET /wp-cron.php HTTP/1.1" 200 131 "-" "Mozilla/5.0"',
            'localhost:80 192.168.240.50 - - [06/Dec/2022:14:02:39 +0000] "GET /wp-content/themes/twentytwentyone/style.css?ver=1.1 HTTP/1.0" 200 152339 "http://leodagan.telecomste.net/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"',
            'localhost:80 192.168.240.50 - - [06/Dec/2022:14:02:39 +0000] "GET /wp-content/themes/twentytwentyone/assets/js/responsive-embeds.js?ver=1.1 HTTP/1.0" 200 1373 "http://leodagan.telecomste.net/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"',
            'localhost:80 192.168.240.50 - - [06/Dec/2022:14:02:40 +0000] "GET /favicon.ico HTTP/1.0" 404 360 "http://leodagan.telecomste.net/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"',
            'localhost:80 192.168.240.50 - - [06/Dec/2022:14:02:55 +0000] "GET / HTTP/1.0" 200 3882 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"',
            'localhost:80 192.168.240.50 - - [06/Dec/2022:14:02:59 +0000] "GET /fuahfzhfua HTTP/1.0" 404 360 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"'
        ]
        self.result = []
        for line in self.list_data:
            ApacheLogLine = LogParser(line)
            self.result.append(ApacheLogLine.getLogLineData())
        self.dataServerInfo = LogInfo(self.result)
    
    def test_getTimeStatusCode(self):
        self.assertEqual(len(self.dataServerInfo.getTimeStatusCode("2022-11-30T00:00:00", "2022-12-07T00:00:00", 404)),2)
    def test_getTimeRemoteClientAccess(self):
        self.assertEqual(len(self.dataServerInfo.getTimeRemoteClientAccess("2022-11-30T00:00:00", "2022-12-07T00:00:00")),5)