import configparser
import paramiko.ssh_exception
import sys, os, string, threading,logging
from models.class_config import Config
from models.class_connexion import Connexion

from models.class_DataServerLog import DataServerLog
monitor0 = Config(0)

connexion = Connexion(monitor0)
print(connexion.client)
client = connexion.client

logging.basicConfig(level=logging.DEBUG,
                    filename=monitor0.hostname+".log",
                    format='%(message)s'
                    )

list_data = []
def get_data(command):
    _, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode("utf-8")
    for line in output.splitlines():
            print(line)

            object = DataServerLog(line)
            list_data.append(object)

            # print(line)
            # logging.info(line)

# args= ["free","top","ps","vmstat","ifconfig -a","cat /proc/meminfo", "cat /proc/cpuinfo","iotop"]
# for i in range(0,len(args)):
#     get_data(args[i])
#     print(i)

get_data("cat /var/log/apache2/other_vhosts_access.log")
#
# print(len(list_data))
# for i in range(0, len(list_data)):
#     print(list_data[i].getLogLineData)

