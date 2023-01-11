class LogInfo:
    """Class that classes infos about errors and client connections """
    def __init__(self):
        self.list_data_log = None

    def set_list_data(self, list_datalog):
        self.list_data_log = list_datalog

    def get_time_status_code(self, statuscode):
        """method that gets the status code error"""
        res_list = []

        for log in self.list_data_log:
            if log['status'] == str(statuscode):
                res = [log["time_received_isoformat"], 1]
            else:
                res = [log["time_received_isoformat"], 0]
            res_list.append(res)

        return res_list

    def get_time_remote_client_access(self):  # date format : 2022-06-01T09:20:28 (iso)
        """method that gets the time remote client access"""
        res_list = []
        for log in self.list_data_log:
            if log['remote_ip'] != "127.0.0.1":
                res = [log["time_received_isoformat"], 1]
            else:
                res = [log["time_received_isoformat"], 0]
            res_list.append(res)

        return res_list

    def get_request_url(self):
        """method that gets the request url"""
        res_list = []
        for log in self.list_data_log:
            if log["request_url"] != '/wp-cron.php':
                res = [log["request_url"], 1]
                res_list.append(res)

        return res_list

    def get_list_data(self):
        """method that gets the list data log"""
        return self.list_data_log
