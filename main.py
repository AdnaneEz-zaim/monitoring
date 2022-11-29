import sys, os, string, threading,configparser
import paramiko

# CONFIGURATION FILE PATH
path_configFile = "config.ini"

# Loading configuration file ----------------------------------------
config = configparser.ConfigParser()
config.read(path_configFile)

machines_hostnames = config['monitored_machines']['hostnames'].split(';')
machines_usernames = config['monitored_machines']['usernames'].split(';')
machines_passwords = config['monitored_machines']['passwords'].split(';')
machines_ports = config['monitored_machines']['ports'].split(';')

print(machines_hostnames)
print(machines_usernames)
print(machines_passwords)
print(machines_ports)
print("Configuration succesfully loaded !")

cmd="ls"
outlock = threading.Lock()
def workon(id):
    _, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode("utf-8")

    with outlock:
        print("")
        print("[" + machines_usernames[id] + "]")
        for line in output.splitlines():
            print(line)


threads = []
machine_id = 0

for h in machines_hostnames:
    t = threading.Thread(
        target=workon,
        args=(machine_id,)
    )
    t.start()
    threads.append(t)
    machine_id = machine_id+1
for t in threads:
    t.join()
