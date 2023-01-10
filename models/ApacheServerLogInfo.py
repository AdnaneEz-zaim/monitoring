from datetime import datetime
from pprint import pprint

class LogInfo:
    """Class that classes infos about errors and client connections """
    def __init__(self):
        self.list_data_log = None
        self.starting_date_statusCode = '2022-12-00T00:00:00'
        self.starting_date_clientConnection = '2022-12-00T00:00:00'

    def set_list_data(self, list_datalog):
        self.list_data_log = list_datalog

    def set_starting_date(self, start_date):  # date format : 2022-06-01T09:20:28 (iso)
        self.starting_date_clientConnection = start_date
        self.starting_date_statusCode = start_date

    def get_time_status_code(self, statuscode):
        """method that gets the time status code"""
        res_list = []


        for log in self.list_data_log:
            print("AVANT")
            print(self.starting_date_statusCode)
            if self.starting_date_statusCode >= log['time_received_isoformat']:
                if log['status'] == str(statuscode):
                    res = [log["time_received_isoformat"],1]
                    res_list.append(res)
                
                else :
                    res = [log["time_received_isoformat"],0]
                    res_list.append(res)

            self.starting_date_statusCode = log["time_received_isoformat"]
            print("Apres")
            print(self.starting_date_statusCode)

        return res_list

    def get_time_remote_client_access(self):  # date format : 2022-06-01T09:20:28 (iso)
        """method that gets the time remote client access"""
        res_list = []
        for log in self.list_data_log:
            if log['remote_ip'] != "127.0.0.1" and self.starting_date_clientConnection < log['time_received_isoformat']:
                res_list.append(log["time_received_isoformat"])
                self.starting_date_clientConnection = log["time_received_isoformat"]
        return res_list

    def get_list_data(self):
        """method that gets the list data log"""
        return self.list_data_log
