class LogInfo:
    """Class that classes infos about errors and client connections """
    def __init__(self, list_datalog):
        self.list_data_log = list_datalog

    def get_time_status_code(self, date_start, date_end, statuscode):  # date format : 2022-06-01T09:20:28 (iso)
        """method that gets the time status code"""
        res_list = []
        for log in self.list_data_log:

            if log['status'] == str(statuscode) and date_start <= log['time_received_isoformat'] <= date_end:
                res_list.append(log["time_received_isoformat"])

        print(res_list)
        return res_list

    def get_time_remote_client_access(self, date_start, date_end):  # date format : 2022-06-01T09:20:28 (iso)
        """method that gets the time remote client access"""
        res_list = []
        for log in self.list_data_log:

            if log['remote_ip'] != "127.0.0.1" and date_start <= log['time_received_isoformat'] <= date_end:
                res_list.append(log["time_received_isoformat"])

        return res_list

    def get_list_data(self):
        """method that gets the list data log"""
        return self.list_data_log
