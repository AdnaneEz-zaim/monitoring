"""
 Main program
 """
import logging
import csv
import os
import time

from models.ConfigurationLoader import Config
from models.Connexion import Connexion
from models.MonitorThreading import MonitorTreading
from models.ApacheServerLogInfo import LogInfo

machineConfiguration = Config()
nbMachineConfiguration = machineConfiguration.getNbMachineConfigurations()
monitors = []
connexions = []
clients = []
logInfos = [] #static
# Init
for m in range(nbMachineConfiguration):
    monitors.append(machineConfiguration.loadMachineConfiguration(m))
    connexions.append(Connexion(monitors[m]))
    clients.append(connexions[m].client)
    logInfos.append(LogInfo())

logging.basicConfig(level=logging.DEBUG,
                    filename="monitors.log",
                    format='%(message)s'
                    )

while True:
    # Starting one thread for each client
    MonitorThreads = []
    for h in range(nbMachineConfiguration):
        t = MonitorTreading(clients[h], h, logInfos[h])
        t.start()
        MonitorThreads.append(t)

    hardwareUsageResults = []
    apache_statusCode_results = []
    apache_clientConnect_results = []

    # Get result from thread when they have finish their tasks
    for t in MonitorThreads:
        t.join()

        # Get Monitoring hardware usage results
        hardwareUsageResults.append(t.hardwareUsage_result)

        # Get monitoring apache log results
        apache_statusCode_results.append(t.apache_statusCode_result)
        apache_clientConnect_results.append(t.apache_clientConnect_result)

    # APACHE LOG -----------------------------------------------------
    # CSV Filling
    for host_id in range(nbMachineConfiguration):
        csv_filename = machineConfiguration.machines_hostnames[host_id] \
                       + '_apacheLog_statusCode404' \
                       + '.csv'

        # Create a csv file in write mode if not already exist
        if not os.path.exists(csv_filename):
            with open(csv_filename, 'w', newline='') as f:
                # Create a CSV writer object
                csv_writer = csv.writer(f)

                # Write header in the first line of the CSV file
                csv_writer.writerow(['Date', 'OCCURRENCE'])


        # Open the csv file created before in add mode
        with open(csv_filename, 'a', newline='') as f:
            # Create a CSV writer object
            csv_writer = csv.writer(f)

            # Write the data in the CSV file
            for value in apache_statusCode_results[host_id]:
                csv_writer.writerow([value, 1])

        csv_filename = machineConfiguration.machines_hostnames[host_id] \
                       + '_apacheLog_clientConnect' \
                       + '.csv'

        # Create a csv file in write mode if not already exist
        if not os.path.exists(csv_filename):
            with open(csv_filename, 'w', newline='') as f:
                # Create a CSV writer object
                csv_writer = csv.writer(f)

                # Write header in the first line of the CSV file
                csv_writer.writerow(['Date', 'OCCURRENCE'])

        # Open the csv file created before in add mode
        with open(csv_filename, 'a', newline='') as f:
            # Create a CSV writer object
            csv_writer = csv.writer(f)

            # Write the data in the CSV file
            for value in apache_clientConnect_results[host_id]:
                csv_writer.writerow([value, 1])

    # Hardware usage ---------------------------------------
    # CSV Filling
    for host_id in range(nbMachineConfiguration):
        csv_filename = machineConfiguration.machines_hostnames[host_id] + '_hardwareUsage' + '.csv'

        # Create a csv file in write mode if not already exist
        if not os.path.exists(csv_filename):
            with open(csv_filename, 'w', newline='') as f:
                # Create a CSV writer object
                csv_writer = csv.writer(f)

                # Write header in the first line of the CSV file
                csv_writer.writerow(['Date','CPU_USAGE','MEM_USAGE','STO_USAGE'])

        # Open the csv file created before in add mode
        with open(csv_filename, 'a', newline='') as f:
            # Create a CSV writer object
            csv_writer = csv.writer(f)

            # Write the data in the CSV file
            csv_writer.writerow(hardwareUsageResults[host_id])

    time.sleep(5)
