import configparser
import paramiko.ssh_exception
import sys, os, string, threading,logging
from models.class_config import Config
from models.class_connexion import Connexion

monitor0 = Config(0)

connexion = Connexion(monitor0)
print(connexion.client)
client = connexion.client


logging.basicConfig(level=logging.DEBUG,
                    filename=monitor0.hostname+".log",
                    
                    format='%(message)s')

def get_data(command):
   
    _, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode("utf-8")
    for line in output.splitlines():
            print(line)
            logging.info(line)


args= ["free","top","ps","vmstat","ifconfig -a","cat /proc/meminfo", "cat /proc/cpuinfo","iotop"]
for i in range(0,len(args)):
    get_data(args[i])
    print(i)
