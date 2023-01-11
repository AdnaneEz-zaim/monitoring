"""
 Main program
 """
import logging
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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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

logging.basicConfig(level=logging.DEBUG,
                    filename="monitors.log",
                    format='%(message)s'
                    )

def createAppLayout(list_csv):
    list_layout = []

    list_layout.append(Dashboard.generate_header_layout())
    # For every monitored machines
    for host_id in range(nbMachineConfiguration):
        # Get all csv file name that start with the currrent machine hostname
        csv_hostname = machineConfiguration.machines_hostnames[host_id]

        # Get csv of current hostname
        filtered_csv_list = [s for s in list_csv[host_id] if s.startswith(csv_hostname)]
        # Get hardware csv of current hostname
        hardware_csv_list = [csvName for csvName in filtered_csv_list if "hardware" in csvName]
        # Get apache csv of current hostname
        apache_csv_list = [csvName for csvName in filtered_csv_list if "apache" in csvName]

        # Generate hostname title layout
        list_layout.append(Dashboard.generate_hostname_title(csv_hostname, "NULL", host_id))

        # Generate layout for hardware usage
        list_layout.append(Dashboard.generate_layout_hardware(hardware_csv_list, "NULL", host_id))

        # Generate layout for apache log
        list_layout.append(Dashboard.generate_layout_apache(apache_csv_list, host_id))

    list_layout.append(Dashboard.generate_interval_component())

    app.layout = Dashboard.generate_app_layout(list_layout)

    print("DASH LAYOUT CREATED")

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
        uptime_serverResults.clear()
        cpuModel_server.clear()

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

        print("-[BACKEND]-DATA SCRAPPING DONE")

        # CSV Filling
        for host_id in range(nbMachineConfiguration):

            fill_csv(csv_fileNames[host_id][0], apache_statusCode_results, host_id)
            fill_csv(csv_fileNames[host_id][1], apache_clientConnect_results, host_id)
            fill_csv(csv_fileNames[host_id][2], apache_requestUrl_results, host_id)
            fill_csv(csv_fileNames[host_id][3], hardwareUsageResults, host_id)

        print("-[BACKEND]-CSV FILLING DONE")

        time.sleep(5)


@app.callback(
        [
        Output('cpu-usage-graph0', 'figure'),
        Output('mem-usage-graph0', 'figure'),
        Output('sto-usage-graph0', 'figure'),
        Output('cpu-usage-graph1', 'figure'),
        Output('mem-usage-graph1', 'figure'),
        Output('sto-usage-graph1', 'figure')
        ],
        [Input('interval-component', 'n_intervals')])
def update_graph_cpu_usage(n_intervals):
    print("-[UI]-UPDATE HARDWARE USAGE GRAPH")
    figures = []
    for host_id in range(nbMachineConfiguration):
        update_figures = Dashboard.update_hardware_usage(csv_fileNames[host_id][3], cpuModel_server[host_id][0])
        for fig in update_figures:
            figures.append(fig)

    return figures

@app.callback(
    [
        Output('error-code-graph0', 'figure'),
        Output('client-connect-graph0', 'figure'),
        Output('requestUrl-graph0', 'figure'),
        Output('error-code-graph1', 'figure'),
        Output('client-connect-graph1', 'figure'),
        Output('requestUrl-graph1', 'figure')
    ],
    [
        Input('interval-component','n_intervals')
    ]
)
def update_graph_apache(n_intervals):
    print("-[UI]-UPDATE APACHE LOG GRAPH")
    figures = []
    for host_id in range(nbMachineConfiguration):

        csv_hostname = machineConfiguration.machines_hostnames[host_id]

        # Get csv of current hostname
        filtered_csv_list = [s for s in csv_fileNames[host_id] if s.startswith(csv_hostname)]

        # Get apache csv of current hostname
        apache_csv_list = [csvName for csvName in filtered_csv_list if "apache" in csvName]

        update_figures = Dashboard.update_apache_log(apache_csv_list, host_id)
        for fig in update_figures:
            figures.append(fig)

    return figures


@app.callback(
    [
        Output('uptime0', 'children'),
        Output('uptime1', 'children')
    ],
    [
        Input('interval-component','n_intervals')
    ]
)
def update_uptime(n_intervals):
    print("-[UI]-UPDATE UPTIME ---")
    childrens = []
    for host_id in range(nbMachineConfiguration):
        childrens.append(Dashboard.update_uptime(uptime_serverResults[host_id][0]))
    return childrens


# Init the data scrapper thread
dataScrapperThread = threading.Thread(target=get_data)
# Start the data scrapper thread
dataScrapperThread.start()

createAppLayout(csv_fileNames)
app.run_server(debug=True)

