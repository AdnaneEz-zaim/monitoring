"""Class to parse the log files we use"""
from pprint import pprint
import apache_log_parser


class LogParser:
    """ Class that parses the info from the log files we use"""
    def __init__(self, raw_line):
        self.line_parser = apache_log_parser.make_parser("%h %a %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")
        self.log_line_data = self.line_parser(raw_line)

    def get_log_line_data(self):
        """method to get a line from the datas"""
        return self.log_line_data
