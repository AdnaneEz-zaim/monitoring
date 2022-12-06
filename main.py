"""
 Main program
 """
import logging
from models.class_config import Config
from models.class_connexion import Connexion
from models.class_ApacheServerLogParser import LogParser
from models.class_ApacheServerLogInfo import LogInfo

monitor0 = Config(0)
monitor1 = Config(1)

connexion = Connexion(monitor0)
client = connexion.client

logging.basicConfig(level=logging.DEBUG,
                    filename=monitor0.hostname + ".log",
                    format='%(message)s'
                    )

list_data = []


def get_data(command):
    result = []
    _, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode("utf-8")
    error = stderr.read().decode("utf-8")
    for line in output.splitlines():
        print(line)
        ApacheLogLine = LogParser(line)
        result.append(ApacheLogLine.getLogLineData())
    return result


# args= ["free","top","ps","vmstat","ifconfig -a","cat /proc/meminfo", "cat /proc/cpuinfo","iotop"]
# for i in range(0,len(args)):
#     get_data(args[i])
#     print(i)

list_data = get_data("cat /var/log/apache2/other_vhosts_access.log")
dataServerInfo = LogInfo(list_data)

print("Time when 404 error occurred in interval : ",
      dataServerInfo.getTimeStatusCode("2022-11-30T00:00:00", "2022-12-07T00:00:00", 404))
print("Time when remote client connection occurred : ",
      dataServerInfo.getTimeRemoteClientAccess("2022-11-30T00:00:00", "2022-12-02T00:00:00"))
