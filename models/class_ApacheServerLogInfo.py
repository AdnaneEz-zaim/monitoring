class LogInfo:

    def __init__(self, list_datalog):
        self.list_dataLog = list_datalog

    def getTimeStatusCode(self, date_start, date_end, statuscode):  # date format : 2022-06-01T09:20:28 (iso)

        res_list = []
        for log in self.list_dataLog:

            if log['status'] == str(statuscode) and date_start <= log['time_received_isoformat'] <= date_end:
                res_list.append(log["time_received_isoformat"])

        print(res_list)
        return res_list

    def getTimeRemoteClientAccess(self, date_start, date_end):  # date format : 2022-06-01T09:20:28 (iso)

        res_list = []
        for log in self.list_dataLog:

            if log['remote_ip'] != "127.0.0.1" and date_start <= log['time_received_isoformat'] <= date_end:
                res_list.append(log["time_received_isoformat"])

        return res_list

    def getListData(self):
        return self.list_dataLog
