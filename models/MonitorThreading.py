import threading
from datetime import datetime
from models.ApacheServerLogParser import LogParser


def appendDataLine(data):
    res = []
    for line in data.splitlines():
        res.append(line)
    return res

class MonitorTreading(threading.Thread):
    def __init__(self, client, id, logInfo):
        threading.Thread.__init__(self)
        self.client = client
        self.id = id
        self.apache_statusCode_result = None
        self.apache_clientConnect_result = None
        self.apache_requestUrl_result = None
        self.hardwareUsage_result = None
        self.uptime_result = None
        self.CPU_name_result = None
        self.logInfo = logInfo

    def run(self):
        # The method workon will be launch in a thread
        self.workon_apache()
        self.workon_hardwareUsage()
        self.workon_uptime()
        self.workon_CPU_name()

    def get_data(self, command):
        """Return the output of the command execute on the remote monitor.
        Parameters:
            command : The command to execute on the remote monitor
        Returns:
            The output of the command
        """

        _, stdout, stderr = self.client.exec_command(command)
        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")
        return output

    def workon_apache(self):
        """ get apache log data and parsing them """
        result = []
        output = self.get_data("cat /var/log/apache2/other_vhosts_access.log")
        for line in output.splitlines():
            # print(line)
            apache_log_line = LogParser(line)
            result.append(apache_log_line.get_log_line_data())

        # Get info from result
        self.logInfo.set_list_data(result)

        # Find final result
        self.apache_statusCode_result = self.logInfo.get_time_status_code(404)
        self.apache_clientConnect_result = self.logInfo.get_time_remote_client_access()
        self.apache_requestUrl_result = self.logInfo.get_request_url()


    def workon_hardwareUsage(self):
        date = datetime.now()

        # Memory Usage
        res = appendDataLine(self.get_data("free"))[1].split()
        mem_used = float(res[2]) / float(res[1]) * 100

        # CPU Usage
        cpu_used = float(
            appendDataLine(self.get_data("echo " + '"$[100-$(vmstat 1 2|tail -1|awk ' + "'{print $15}')]" + '"'))[0])

        # Storage Usage
        sto_used = float(appendDataLine(self.get_data("df -h"))[1].split()[4].replace("%", ""))

        # Join data
        self.hardwareUsage_result = [date, cpu_used, mem_used, sto_used]

    def workon_uptime(self):
        uptime = appendDataLine(self.get_data("uptime | awk -F'( |,|:)+' '{print $6,$7}'"))

        # Join data
        self.uptime_result = uptime

    def workon_CPU_name(self):
        cpu_name = appendDataLine(self.get_data("grep \"model name\" /proc/cpuinfo | head -1 | cut -d \" \" -f 3-"))
        self.CPU_name_result = cpu_name
