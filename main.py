"""
 Main program
 """
import logging
from models.class_config import Config
from models.class_connexion import Connexion
from models.class_ApacheServerLogParser import LogParser
from models.class_ApacheServerLogInfo import LogInfo

machineConfiguration = Config()
nbMachineConfiguration = machineConfiguration.getNbMachineConfigurations()
monitors = []
connexions = []
clients = []

for m in range(nbMachineConfiguration):
    monitors.append(machineConfiguration.loadMachineConfiguration(m))
    connexions.append(Connexion(monitors[m]))
    clients.append(connexions[m].client)

    logging.basicConfig(level=logging.DEBUG,
                        filename="monitor" + str(m) + ".log",
                        format='%(message)s'
                        )

    print(monitors[m])
    print(connexions[m])
    print(clients[m])

list_data = []

# def get_data(command):
#     """
#     :param command:
#     :return List:
#     """
#     result = []
#     _, stdout, stderr = client.exec_command(command)
#     output = stdout.read().decode("utf-8")
#     error = stderr.read().decode("utf-8")
#     for line in output.splitlines():
#         print(line)
#         apache_log_line = LogParser(line)
#         result.append(apache_log_line.get_log_line_data())
#     return result


# args= ["free","top","ps","vmstat","ifconfig -a","cat /proc/meminfo", "cat /proc/cpuinfo","iotop"]
# for i in range(0,len(args)):
#     get_data(args[i])
#     print(i)

# list_data = get_data("cat /var/log/apache2/other_vhosts_access.log")
# dataServerInfo = LogInfo(list_data)
#
# print("Time when 402 error occurred in interval : ",
#       dataServerInfo.get_time_status_code("2022-12-12T00:00:00", "2022-12-14T00:00:00", 404))
# print("Time when remote client connection occurred : ",
#       dataServerInfo.get_time_remote_client_access("2022-12-12T00:00:00", "2022-12-14T00:00:00"))

# print(len(list_data))
# for i in range(0, len(list_data)):
#     print(list_data[i].getLogLineData)
