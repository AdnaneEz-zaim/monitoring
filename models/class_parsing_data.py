from datetime import datetime


class Parsing_data:

    def __init__(self, client):
        self.client= client

    def get_data(self, command):
        """
        :param command:
        :return List:
        """

        _, stdout, stderr = self.client.exec_command(command)
        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")
        res = []
        for line in output.splitlines():
            print(line)
            res.append(line)
        return res


    def get_memory(self):
        res = self.get_data("free")[1].split()
        p_used = float(res[2])/float(res[1])*100
        date = datetime.now()
        return p_used, date

    def get_cpu(self):
        cpu_used = float(self.get_data("echo " + '"$[100-$(vmstat 1 2|tail -1|awk ' + "'{print $15}')]"+'"')[0])
        date = datetime.now()
        return cpu_used, date

    def get_storage(self):
        s_used = float(self.get_data("df -h")[1].split()[4].replace("%", ""))
        date = datetime.now()
        return s_used, date