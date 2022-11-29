import apache_log_parser
from pprint import pprint

class DataServerLog:

    def __init__(self, raw_line):

        self.line_parser=apache_log_parser.make_parser("%a %A %r %t %T")
        self.log_line_data = self.line_parser(raw_line)
        pprint(self.log_line_data)


    def getLogLineData(self):
        return self.log_line_data
