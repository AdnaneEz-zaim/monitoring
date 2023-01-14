"""
 Main program
 """
import threading
import time
import dash
from dash.dependencies import Input, Output

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
csv_fileNames = [[] for _ in range(nbMachineConfiguration)]
uptime_serverResults = [None] * nbMachineConfiguration
cpuModel_server = [None] * nbMachineConfiguration
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True)
app.title = "GROUP 6 Server Monitoring Dashboard"

# Init
for h in range(nbMachineConfiguration):
    monitors.append(machineConfiguration.loadMachineConfiguration(h))
    connexions.append(Connexion(monitors[h]))
    clients.append(connexions[h].client)
    logInfos.append(LogInfo())

    # CREATE CSV NAMES
    # APACHE LOG -----------------------------------------------------
    # CSV Error code
    csv_filename = machineConfiguration.machines_hostnames[h] \
                   + '_apacheLog_statusCode404' \
                   + '.csv'
    csv_fileNames[h].append(csv_filename)

    # CSV Client connect
    csv_filename = machineConfiguration.machines_hostnames[h] \
                   + '_apacheLog_clientConnect' \
                   + '.csv'
    csv_fileNames[h].append(csv_filename)

    # CSV URL request
    csv_filename = machineConfiguration.machines_hostnames[h] \
                   + '_apacheLog_requestUrl' \
                   + '.csv'
    csv_fileNames[h].append(csv_filename)

    # Hardware usage ---------------------------------------
    csv_filename = machineConfiguration.machines_hostnames[h] \
                   + '_hardwareUsage' \
                   + '.csv'
    csv_fileNames[h].append(csv_filename)


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

        # Get result from thread when they have finish their tasks
        hostid = 0
        for t in MonitorThreads:
            t.join()

            # Get Monitoring hardware usage results
            hardwareUsageResults.append(t.hardwareUsage_result)

            uptime_serverResults[hostid] = t.uptime_result
            cpuModel_server[hostid] = t.CPU_name_result

            # Get monitoring apache log results
            apache_statusCode_results.append(t.apache_statusCode_result)
            apache_clientConnect_results.append(t.apache_clientConnect_result)
            apache_requestUrl_results.append(t.apache_requestUrl_result)
            hostid = hostid + 1

        print("-[BACKEND]-DATA SCRAPPING DONE")


        # CSV Filling
        for host_id in range(nbMachineConfiguration):
            fill_csv(csv_fileNames[host_id][0], apache_statusCode_results, host_id)
            fill_csv(csv_fileNames[host_id][1], apache_clientConnect_results, host_id)
            fill_csv(csv_fileNames[host_id][2], apache_requestUrl_results, host_id)
            fill_csv(csv_fileNames[host_id][3], hardwareUsageResults, host_id)

        print("-[BACKEND]-CSV FILLING DONE")

        time.sleep(5)


outputs_hardwareUsage = []
for i in range(nbMachineConfiguration):
    outputs_hardwareUsage.append(Output(f'cpu-usage-graph{i}', 'figure'))
    outputs_hardwareUsage.append(Output(f'mem-usage-graph{i}', 'figure'))
    outputs_hardwareUsage.append(Output(f'sto-usage-graph{i}', 'figure'))


@app.callback(outputs_hardwareUsage, [Input('interval-component', 'n_intervals')])
def update_graph_cpu_usage(n_intervals):
    figures = []
    for host_id in range(nbMachineConfiguration):
        update_figures = Dashboard.update_hardware_usage(csv_fileNames[host_id][3], cpuModel_server[host_id][0])
        for fig in update_figures:
            figures.append(fig)

    return figures


outputs_apache = []
for i in range(nbMachineConfiguration):
    outputs_apache.append(Output(f'error-code-graph{i}', 'figure'))
    outputs_apache.append(Output(f'client-connect-graph{i}', 'figure'))
    outputs_apache.append(Output(f'requestUrl-graph{i}', 'figure'))


@app.callback(outputs_apache, [Input('interval-component', 'n_intervals')])
def update_graph_apache(n_intervals):
    figures = []
    for host_id in range(nbMachineConfiguration):
        csv_hostname = machineConfiguration.machines_hostnames[host_id]
        filtered_csv_list = [s for s in csv_fileNames[host_id] if s.startswith(csv_hostname)]
        apache_csv_list = [csvName for csvName in filtered_csv_list if "apache" in csvName]
        update_figures = Dashboard.update_apache_log(apache_csv_list, host_id)
        for fig in update_figures:
            figures.append(fig)
    return figures


outputs_uptime = []
for i in range(nbMachineConfiguration):
    outputs_uptime.append(Output(f'uptime{i}', 'children'))


@app.callback(outputs_uptime, [Input('interval-component', 'n_intervals')])
def update_uptime(n_intervals):
    childrens = []
    for host_id in range(nbMachineConfiguration):
        childrens.append(Dashboard.update_uptime(uptime_serverResults[host_id][0]))
    return childrens


# Init the data scrapper thread
dataScrapperThread = threading.Thread(target=get_data)
# Start the data scrapper thread
dataScrapperThread.start()

app.layout = Dashboard.generate_header_layout()
app.run_server(debug=True)
