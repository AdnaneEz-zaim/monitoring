"""
 Main program
 """
import logging
import threading
import time
import dash

from models.ConfigurationLoader import Config
from models.Connexion import Connexion
from models.MonitorThreading import MonitorTreading
from models.ApacheServerLogInfo import LogInfo
from models.CSVFiller import fill_csv
import models.Dash as Dashboard

machineConfiguration = Config()
nbMachineConfiguration = machineConfiguration.getNbMachineConfigurations()
monitors = []
connexions = []
clients = []
logInfos = []

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#F0F8FF',
    'text': '#00008B'
}

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


def get_data():
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
        apache_requestUrl_results = []
        uptime_serverResults = []
        cpuModel_server = []

        # Get result from thread when they have finish their tasks
        for t in MonitorThreads:
            t.join()

            # Get Monitoring hardware usage results
            hardwareUsageResults.append(t.hardwareUsage_result)

            # Get uptime
            uptime_serverResults.append(t.uptime_result)

            # Get CPU_name
            cpuModel_server.append(t.CPU_name_result)

            # Get monitoring apache log results
            apache_statusCode_results.append(t.apache_statusCode_result)
            apache_clientConnect_results.append(t.apache_clientConnect_result)
            apache_requestUrl_results.append(t.apache_requestUrl_result)

        print("DATA SCRAPPING DONE")

        # CSV Filling
        csv_fileNames = []
        for host_id in range(nbMachineConfiguration):
            # APACHE LOG -----------------------------------------------------
            # CSV Error code
            csv_filename = machineConfiguration.machines_hostnames[host_id] \
                           + '_apacheLog_statusCode404' \
                           + '.csv'
            csv_fileNames.append(csv_filename)

            fill_csv(csv_filename, apache_statusCode_results, host_id)

            # CSV Client connect
            csv_filename = machineConfiguration.machines_hostnames[host_id] \
                           + '_apacheLog_clientConnect' \
                           + '.csv'
            csv_fileNames.append(csv_filename)

            fill_csv(csv_filename, apache_clientConnect_results, host_id)

            # CSV URL request
            csv_filename = machineConfiguration.machines_hostnames[host_id] \
                           + '_apacheLog_requestUrl' \
                           + '.csv'
            csv_fileNames.append(csv_filename)

            fill_csv(csv_filename, apache_requestUrl_results, host_id)

            # Hardware usage ---------------------------------------
            csv_filename = machineConfiguration.machines_hostnames[host_id] + '_hardwareUsage' + '.csv'
            csv_fileNames.append(csv_filename)

            fill_csv(csv_filename, hardwareUsageResults, host_id)

        print("CSV FILLING DONE")

        update_server_metrics(csv_fileNames, uptime_serverResults, cpuModel_server)
        time.sleep(5)


def update_server_metrics(list_csv, uptime_serverResults, cpuModel_server):
    list_layout = [Dashboard.genetate_header_layout()]

    # For every monitored machines
    for host_id in range(nbMachineConfiguration):

        # Get all csv file name that start with the currrent machine hostname
        csv_hostname = machineConfiguration.machines_hostnames[host_id]
        filtered_csv_list = [s for s in list_csv if s.startswith(csv_hostname)]

        # For every csv in this list
        for csv_name in filtered_csv_list:
            list_layout.append(
                Dashboard.generate_layout_brick(csv_name, uptime_serverResults, cpuModel_server, host_id))

    app.layout = Dashboard.generate_app_layout(list_layout)

    print("DASH UPDATED")


# Init the data scrapper thread
dataScrapperThread = threading.Thread(target=get_data)
# Start the data scrapper thread
dataScrapperThread.start()
app.run_server()
