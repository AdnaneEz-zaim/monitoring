import apache_log_parser
from pprint import pprint


class LogParser:

    def __init__(self, raw_line):
        self.line_parser = apache_log_parser.make_parser("%h %a %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")
        self.log_line_data = self.line_parser(raw_line)
        #pprint(self.log_line_data)

    def getLogLineData(self):
        return self.log_line_data
