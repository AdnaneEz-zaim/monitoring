"""
 Main program
 """
import threading
import time
import dash
from dash.dependencies import Input, Output, State
from models.ConfigurationLoader import Config
from models.Connexion import Connexion
from models.MonitorThreading import MonitorTreading
from models.ApacheServerLogInfo import LogInfo
from models.CSVFiller import fill_csv
import models.Dash as Dashboard

# Init variables
machineConfiguration = Config()
nbMachineConfiguration = machineConfiguration.getNbMachineConfigurations()
monitors = []
connexions = []
clients = []
logInfos = []
csv_fileNames = [[] for _ in range(nbMachineConfiguration)]
uptime_serverResults = [None] * nbMachineConfiguration
cpuModel_server = [None] * nbMachineConfiguration

outputs_hardwareUsage = []
outputs_apache = []
outputs_uptime = []

# Init
for h in range(machineConfiguration.getNbMachineConfigurations()):
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


def update_variables():
    """
    Update variables when new configuratio is added to config.ini
    """
    global machineConfiguration, nbMachineConfiguration, \
        monitors, connexions, clients, logInfos, csv_fileNames, \
        uptime_serverResults, cpuModel_server
    # Init variables
    machineConfiguration = Config()
    nbMachineConfiguration = machineConfiguration.getNbMachineConfigurations()
    monitors = []
    connexions = []
    clients = []
    logInfos = []
    csv_fileNames = [[] for _ in range(nbMachineConfiguration)]
    uptime_serverResults = [None] * nbMachineConfiguration
    cpuModel_server = [None] * nbMachineConfiguration

    # Init
    for h in range(machineConfiguration.getNbMachineConfigurations()):
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
    """ gather data from data scrapper threads"""
    while True:
        # Starting one thread for each client
        MonitorThreads = []
        for h in range(machineConfiguration.getNbMachineConfigurations()):
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
        for host_id in range(machineConfiguration.getNbMachineConfigurations()):
            fill_csv(csv_fileNames[host_id][0], apache_statusCode_results, host_id)
            fill_csv(csv_fileNames[host_id][1], apache_clientConnect_results, host_id)
            fill_csv(csv_fileNames[host_id][2], apache_requestUrl_results, host_id)
            fill_csv(csv_fileNames[host_id][3], hardwareUsageResults, host_id)

        print("-[BACKEND]-CSV FILLING DONE")

        time.sleep(5)


# Init the data scrapper thread
dataScrapperThread = threading.Thread(target=get_data)
# Start the data scrapper thread
dataScrapperThread.start()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True, suppress_callback_exceptions=True)
app.title = "GROUP 6 Server Monitoring Dashboard"
app.layout = Dashboard.generate_header_layout()


@app.callback(
    Output('server-graph', 'children'),
    [
        Input('refresh-graph-button'),
        Input('interval-component')
    ],
    State('server-graph')
)
def display_graphServerMonitoring():
    print("ADD GRAPH MONITORING")
    machineConfig = Config()
    children = []
    for host in range(machineConfig.getNbMachineConfigurations()):
        # Title
        new_titleHostname = Dashboard.generate_hostname_title(machineConfig.machines_hostnames[host],
                                                              uptime_serverResults, host)
        # Hardware graph
        new_graphHardware = Dashboard.generate_layout_hardware(csv_fileNames[host][3], cpuModel_server, host)

        # Apache Graph
        csv_hostname = machineConfig.machines_hostnames[host]
        filtered_csv_list = [s for s in csv_fileNames[host] if s.startswith(csv_hostname)]
        apache_csv_list = [csvName for csvName in filtered_csv_list if "apache" in csvName]
        new_graphApache = Dashboard.generate_layout_apache(apache_csv_list, host)

        # Append Childrens
        children.append(new_titleHostname)
        children.append(new_graphHardware)
        children.append(new_graphApache)

    return children


@app.callback(
    Output('server-overview', 'children'),
    [
        Input('refresh-panel-button'),
    ],
    State('server-overview')
)
def display_panelServerOverview():
    print("ADD PANELS OVERVIEW")
    machineConfig = Config()

    children = []
    for host in range(machineConfig.getNbMachineConfigurations()):
        new_panel = Dashboard.generate_serverOverviewPanel(machineConfig.machines_hostnames[host], uptime_serverResults,
                                                           host)
        children.append(new_panel)

    return children


@app.callback(Output('output', 'children'),
              [
                  Input('submit-button', 'n_clicks'),
                  Input('input-hostname', 'value'),
                  Input('input-username', 'value'),
                  Input('input-password', 'value'),
                  Input('input-port', 'value')
              ]
              )
def get_input_value(n_clicks, inputHostname, inputUsername, inputPassword, inputPort):
    print("SHOW INPUT")
    if n_clicks == 0:
        return ''
    else:
        machineConfiguration.setMachineConfiguration(inputHostname, inputUsername, inputPassword, inputPort)
        update_variables()
        return f'Name: {inputHostname}, Username: {inputUsername}, Password: {inputPassword}, Port: {inputPort}'


app.run_server(debug=True)
