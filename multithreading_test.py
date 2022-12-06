""" Fichier test multithreading"""

import threading, configparser  

# CONFIGURATION FILE PATH

PATH_CONFIGFILE = "config.ini"

# Loading configuration file ----------------------------------------
config = configparser.ConfigParser()
config.read(PATH_CONFIGFILE)

machines_hostnames = config['monitored_machines']['hostnames'].split(';')
machines_usernames = config['monitored_machines']['usernames'].split(';')
machines_passwords = config['monitored_machines']['passwords'].split(';')
machines_ports = config['monitored_machines']['ports'].split(';')

print(machines_hostnames)
print(machines_usernames)
print(machines_passwords)
print(machines_ports)
print("Configuration succesfully loaded !")

CMD = "ls"
outlock = threading.Lock()
def workon(id):
    """ Method wich executes commands on the ID machine"""
    _, stdout = ssh.exec_command(CMD)
    output = stdout.read().decode("utf-8")

    with outlock:
        print("")
        print("[" + machines_usernames[id] + "]")
        for line in output.splitlines():
            print(line)


threads = []
MACHINE_ID = 0

for h in machines_hostnames:
    t = threading.Thread(
        target=workon,
        args=(MACHINE_ID,)
    )
    t.start()
    threads.append(t)
    MACHINE_ID = MACHINE_ID+1
for t in threads:
    t.join()
